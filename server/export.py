import csv
import io
import zipfile
from sqlalchemy.orm import Session
from . import models
import sqlite3
import pandas as pd
import os

def export_dataset_to_zip(db: Session, format: str):
    """Generate a ZIP file containing datasets across 4 formats: sql, csv, excel, txt."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        if format == "sql":
            # Direct SQLite dump
            conn = sqlite3.connect('./vc_database.db')
            dump = "\n".join(conn.iterdump())
            conn.close()
            zip_file.writestr("database_dump.sql", dump)
        else:
            # Table aggregations
            tables = {
                "machines": db.query(models.Machine).all(),
                "sessions": db.query(models.Session).all(),
                "snapshots": db.query(models.Snapshot).all(),
                "power_events": db.query(models.PowerEvent).all(),
                "task_results": db.query(models.TaskResult).all()
            }
            
            for name, data in tables.items():
                if not data:
                    continue
                
                model = data[0].__class__
                columns = [column.name for column in model.__table__.columns]
                dict_data = [{col: getattr(row, col) for col in columns} for row in data]
                df = pd.DataFrame(dict_data)
                
                if format == "excel":
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False)
                    zip_file.writestr(f"{name}.xlsx", excel_buffer.getvalue())
                elif format == "txt":
                    zip_file.writestr(f"{name}.txt", df.to_csv(sep='\t', index=False))
                else: # Default format = csv
                    zip_file.writestr(f"{name}.csv", df.to_csv(index=False))
                    
    zip_buffer.seek(0)
    return zip_buffer
