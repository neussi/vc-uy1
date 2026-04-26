import sys
import os

# Add server to path
sys.path.append(os.getcwd())

from server.database import SessionLocal
from server.export import export_dataset_to_zip
import traceback

def run_diag():
    db = SessionLocal()
    formats = ["csv", "excel", "txt", "sql"]
    
    for fmt in formats:
        print(f"Testing format: {fmt}...")
        try:
            buf = export_dataset_to_zip(db, fmt)
            print(f"  Success! Buffer size: {len(buf.getvalue())} bytes")
        except Exception as e:
            print(f"  FAILED for {fmt}:")
            traceback.print_exc()
    db.close()

if __name__ == "__main__":
    run_diag()
