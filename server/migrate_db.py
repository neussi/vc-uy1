
import sqlite3
import os

db_path = "vc_database.db"
if not os.path.exists(db_path):
    # Try server directory if running from root
    db_path = "server/vc_database.db"

if not os.path.exists(db_path):
    print("Base de données non trouvée. Assurez-vous d'être dans le bon répertoire.")
else:
    print(f"Migration de la base de données : {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add features_json column to snapshots table
        cursor.execute("ALTER TABLE snapshots ADD COLUMN features_json TEXT")
        conn.commit()
        print("SUCCESS: La colonne 'features_json' a été ajoutée avec succès.")
        
        # Also clean up old task tables if they still exist
        cursor.execute("DROP TABLE IF EXISTS task_results")
        cursor.execute("DROP TABLE IF EXISTS active_tasks")
        conn.commit()
        print("SUCCESS: Les anciennes tables de tâches ont été supprimées.")
        
        conn.close()
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("INFO: La colonne existe déjà.")
        else:
            print(f"ERROR: {e}")
    except Exception as e:
        print(f"ERROR: {e}")
