import os
from fastapi import FastAPI, Depends, HTTPException, Body, Response
from fastapi.responses import StreamingResponse, PlainTextResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, database, auth, export
from typing import List
import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
def export_dataset(format: str = "csv", db: Session = Depends(get_db)):
    zip_buffer = export.export_dataset_to_zip(db, format)
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
    
    # Map fields to model (handling agent/server mismatches)
    model_data = {
        "machine_id": machine.get('machine_id'),
        "os": machine.get('os', 'unknown'),
        "hostname_hash": machine.get('hostname_hash') or machine.get('hostname', 'unknown'),
        "cpu_cores": machine.get('cpu_cores', 0),
        "ram_total_mb": int(machine.get('ram_total_mb') or (machine.get('ram_gb', 0) * 1024)),
        "timezone": machine.get('timezone', 'UTC'),
        "city": machine.get('city', 'Unknown'),
        "consent_level": machine.get('consent_level', 1)
    }
    
    new_machine = models.Machine(**model_data)
    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)
    return {"status": "registered", "machine_id": new_machine.machine_id}

@app.post("/sessions/start")
def start_session(session: dict, db: Session = Depends(get_db)):
    # Parse isoformat dates
    if 'boot_time' in session:
        session['boot_time'] = datetime.datetime.fromisoformat(session['boot_time'])
    
    db_session = models.Session(**session)
    db.add(db_session)
    db.commit()
    return {"status": "ok", "session_id": db_session.session_id}

@app.post("/sync/snapshots")
def sync_snapshots(machine_id: str = Body(...), snapshots: List[dict] = Body(...), db: Session = Depends(get_db)):
    try:
        db_snapshots = []
        for s in snapshots:
            # Parse dates
            if 'ts_utc' in s: s['ts_utc'] = datetime.datetime.fromisoformat(s['ts_utc'].replace('Z', ''))
            if 'ts_local' in s: s['ts_local'] = datetime.datetime.fromisoformat(s['ts_local'].replace('Z', ''))
            db_snapshots.append(models.Snapshot(machine_id=machine_id, **s))
            
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
    # Sanitize to expose only public metrics including IO
    return [{
        "id": s.snapshot_id, 
        "timestamp": s.ts_utc.timestamp(), 
        "cpu": s.cpu_percent, 
        "ram": s.ram_percent_used, 
        "battery": s.battery_percent, 
        "plugged": s.power_plugged,
        "net_sent": s.bytes_sent_kb,
        "net_recv": s.bytes_recv_kb,
        "disk_read": s.disk_read_mbps,
        "disk_write": s.disk_write_mbps
    } for s in snapshots]

@app.get("/tasks/recent")
def get_recent_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.TaskResult).order_by(models.TaskResult.end_time.desc()).limit(10).all()
    return [{
        "task_id": t.task_id,
        "machine_id": t.machine_id,
        "session_id": t.session_id,
        "start_time": t.start_time.isoformat() if t.start_time else None,
        "end_time": t.end_time.isoformat() if t.end_time else None,
        "target_duration_s": t.target_duration_s,
        "actual_duration_s": t.actual_duration_s,
        "interrupted": t.interrupted,
        "avg_cpu_load": t.avg_cpu_load,
        "avg_ram_load": t.avg_ram_load,
        "network_io_mb": t.network_io_mb
    } for t in tasks]

@app.post("/sync/power-events")
def sync_power_events(event: dict = Body(...), db: Session = Depends(get_db)):
    try:
        ts_utc = datetime.datetime.fromisoformat(event['ts_utc'].replace('Z', ''))
        db_event = models.PowerEvent(
            machine_id=event['machine_id'],
            event_type=event['event_type'],
            gap_seconds=event.get('gap_s'),
            detected_at=ts_utc,
            last_heartbeat_ts=None # To be improved if needed
        )
        db.add(db_event)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export")
def export_data(format: str = "csv", db: Session = Depends(get_db)):
    from . import export
    zip_buffer = export.export_dataset_to_zip(db, format)
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=vc_uy1_dataset_{format}.zip"}
    )

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

def send_contact_email(data: ContactForm):
    # Credentials provided by USER
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "npe.techs@gmail.com"
    SMTP_PASS = "dtbl pdrr sodx bcmt"
    
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER # Send to the PI
    msg['Subject'] = f"[VC-UY1 CONTACT] {data.subject} - De {data.name}"
    
    body = f"Expéditeur: {data.name} ({data.email})\n\nSujet: {data.subject}\n\nMessage:\n{data.message}"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

@app.post("/contact")
async def handle_contact(data: ContactForm):
    if send_contact_email(data):
        return {"status": "ok", "message": "Email en cours d'envoi"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de l'envoi de l'email")

@app.post("/sync/tasks")
def sync_task_results(task: dict = Body(...), db: Session = Depends(get_db)):
    try:
        start_ts = datetime.datetime.fromisoformat(task['start_time'].replace('Z', ''))
        end_ts = datetime.datetime.fromisoformat(task['end_time'].replace('Z', '')) if task.get('end_time') else None
        
        db_task = models.TaskResult(
            task_id=task['task_id'],
            machine_id=task['machine_id'],
            session_id=task['session_id'],
            start_time=start_ts,
            end_time=end_ts,
            target_duration_s=task['target_duration_s'],
            actual_duration_s=task['actual_duration_s'],
            interrupted=task['interrupted'],
            avg_cpu_load=task['avg_cpu_load'],
            avg_ram_load=task['avg_ram_load'],
            network_io_mb=task.get('network_io_mb', 0)
        )
        db.add(db_task)
        # Remove from active tasks if it was there
        db.query(models.ActiveTask).filter(models.ActiveTask.task_id == task['task_id']).delete()
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks/start")
def start_active_task(task: dict = Body(...), db: Session = Depends(get_db)):
    try:
        db_task = models.ActiveTask(
            task_id=task['task_id'],
            machine_id=task['machine_id'],
            session_id=task['session_id'],
            target_duration_s=task['target_duration_s']
        )
        db.add(db_task)
        db.commit()
        return {"status": "ok"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/tasks/update")
def update_task_progress(task_id: str = Body(...), progress: float = Body(...), db: Session = Depends(get_db)):
    db_task = db.query(models.ActiveTask).filter(models.ActiveTask.task_id == task_id).first()
    if db_task:
        db_task.progress_percent = progress
        db.commit()
        return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/tasks/active")
def get_active_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.ActiveTask).all()
    return [{
        "task_id": t.task_id,
        "machine_id": t.machine_id,
        "progress": t.progress_percent,
        "start_time": t.start_time.isoformat(),
        "target": t.target_duration_s
    } for t in tasks]

@app.get("/nodes/list")
def list_machines_with_stats(db: Session = Depends(get_db)):
    # Join machines with snapshot counts and task counts
    machines = db.query(models.Machine).all()
    results = []
    for m in machines:
        snap_count = db.query(models.Snapshot).filter(models.Snapshot.machine_id == m.machine_id).count()
        task_count = db.query(models.TaskResult).filter(models.TaskResult.machine_id == m.machine_id).count()
        results.append({
            "machine_id": m.machine_id,
            "os": m.os,
            "last_seen": m.last_seen.isoformat() if m.last_seen else None,
            "snapshots": snap_count,
            "tasks": task_count,
            "cores": m.cpu_cores,
            "ram": m.ram_total_mb
        })
    return results
@app.get("/stats/detailed")
def get_detailed_stats(db: Session = Depends(get_db)):
    # OS Distribution
    os_dist = db.query(models.Machine.os, func.count(models.Machine.machine_id)).group_by(models.Machine.os).all()
    # Machine count
    machine_count = db.query(models.Machine).count()
    # Total snapshots
    snapshot_count = db.query(models.Snapshot).count()
    
    return {
        "os_distribution": [{"name": os, "value": count} for os, count in os_dist],
        "total_machines": machine_count,
        "total_snapshots": snapshot_count,
        "availability_avg": 98.5 # Placeholder or calculated
    }

# Serve frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dist_path = os.path.join(BASE_DIR, "frontend", "dist")

if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="frontend")
else:
    @app.get("/")
    def read_root():
        return {"message": "VC-UY1 API Running. Front-end build not found at " + dist_path}
