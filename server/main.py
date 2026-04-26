import os
from fastapi import FastAPI, Depends, HTTPException, Body, Response
from fastapi.responses import StreamingResponse, PlainTextResponse
from sqlalchemy.orm import Session
from . import models, database, auth, export
from typing import List
import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
import os

app = FastAPI(title="VC-UY1 Central Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

@app.get("/debug/diag", response_class=PlainTextResponse)
def get_diagnostics():
    diag_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diag_result.txt")
    if os.path.exists(diag_path):
        with open(diag_path, "r") as f:
            return f.read()
    return "Diagnostic file NOT FOUND at " + diag_path

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Simple hardcoded admin check for research purposes
    if form_data.username == "admin" and form_data.password == "vc-uy1-recherche":
        access_token = auth.create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

@app.get("/export/dataset")
def export_dataset(db: Session = Depends(get_db)):
    zip_buffer = export.export_dataset_to_zip(db)
    return StreamingResponse(
        zip_buffer, 
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=vc_uy1_dataset_{datetime.datetime.now().strftime('%Y%m%d')}.zip"}
    )

@app.post("/register")
def register_machine(machine: dict, db: Session = Depends(get_db)):
    db_machine = db.query(models.Machine).filter(models.Machine.machine_id == machine['machine_id']).first()
    if db_machine:
        return {"status": "exists", "machine_id": db_machine.machine_id}
    new_machine = models.Machine(**machine)
    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)
    return {"status": "registered", "machine_id": new_machine.machine_id}

@app.post("/sync/snapshots")
def sync_snapshots(machine_id: str = Body(...), snapshots: List[dict] = Body(...), db: Session = Depends(get_db)):
    try:
        db_snapshots = [models.Snapshot(machine_id=machine_id, **s) for s in snapshots]
        db.add_all(db_snapshots)
        db.commit()
        return {"status": "ok", "saved_rows": len(snapshots)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/live")
def get_live_stats(db: Session = Depends(get_db)):
    machine_count = db.query(models.Machine).count()
    snapshot_count = db.query(models.Snapshot).count()
    # F1-Score and size are static model properties, but we serve them here so the UI is fully dynamic
    return {
        "active_machines": machine_count,
        "snapshots": snapshot_count,
        "f1_score": "82.4%",
        "footprint": "< 8MB"
    }

@app.get("/feed")
def get_live_data_feed(db: Session = Depends(get_db)):
    # Returns the last 50 data points strictly for the live visualization on homepage
    snapshots = db.query(models.Snapshot).order_by(models.Snapshot.snapshot_id.desc()).limit(50).all()
    # Sanitize to expose only public metrics
    return [{"id": s.snapshot_id, "timestamp": s.timestamp, "cpu": s.cpu_percent, "ram": s.ram_percent, "battery": s.battery_percent, "plugged": s.power_plugged} for s in snapshots]

# Serve frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dist_path = os.path.join(BASE_DIR, "frontend", "dist")

if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="frontend")
else:
    @app.get("/")
    def read_root():
        return {"message": "VC-UY1 API Running. Front-end build not found at " + dist_path}
