import csv
import io
import zipfile
from sqlalchemy.orm import Session
from . import models
import os

def export_dataset_to_zip(db: Session):
    """Generate a ZIP file containing CSVs of all research tables."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # Export Machines
        machines = db.query(models.Machine).all()
        zip_file.writestr("machines.csv", generate_csv(machines, models.Machine))
        
        # Export Sessions
        sessions = db.query(models.Session).all()
        zip_file.writestr("sessions.csv", generate_csv(sessions, models.Session))
        
        # Export Snapshots
        snapshots = db.query(models.Snapshot).all()
        zip_file.writestr("snapshots.csv", generate_csv(snapshots, models.Snapshot))
        
        # Export Power Events
        power_events = db.query(models.PowerEvent).all()
        zip_file.writestr("power_events.csv", generate_csv(power_events, models.PowerEvent))
        
    zip_buffer.seek(0)
    return zip_buffer

def generate_csv(data, model):
    """Helper to convert SQLAlchemy results to CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    columns = [column.name for column in model.__table__.columns]
    writer.writerow(columns)
    
    # Rows
    for row in data:
        writer.writerow([getattr(row, col) for col in columns])
        
    return output.getvalue()
