
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
        try:
            cursor.execute("ALTER TABLE snapshots ADD COLUMN features_json TEXT")
            conn.commit()
            print("SUCCESS: La colonne 'features_json' a été ajoutée avec succès.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("INFO: La colonne 'features_json' existe déjà.")
            else:
                raise e

        # Add preferences columns to machines table
        try:
            cursor.execute("ALTER TABLE machines ADD COLUMN allowed_days TEXT")
            cursor.execute("ALTER TABLE machines ADD COLUMN allowed_slots TEXT")
            cursor.execute("ALTER TABLE machines ADD COLUMN contrib_mode TEXT DEFAULT 'total'")
            conn.commit()
            print("SUCCESS: Les colonnes de préférences ont été ajoutées avec succès.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("INFO: Les colonnes de préférences existent déjà.")
            else:
                raise e

        # Add new static machines columns
        try:
            cursor.execute("ALTER TABLE machines ADD COLUMN cpu_model TEXT")
            cursor.execute("ALTER TABLE machines ADD COLUMN cpu_cores_physical INTEGER")
            cursor.execute("ALTER TABLE machines ADD COLUMN disk_total_gb REAL")
            conn.commit()
            print("SUCCESS: Les colonnes statiques additionnelles ont été ajoutées à la table 'machines'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("INFO: Les colonnes statiques de la table 'machines' existent déjà.")
            else:
                raise e

        # Add new dynamic snapshots columns
        new_snap_cols = [
            ("swap_percent", "REAL"),
            ("swap_total_mb", "INTEGER"),
            ("swap_used_mb", "INTEGER"),
            ("ram_used_mb", "INTEGER"),
            ("disk_percent_used", "REAL"),
            ("disk_used_gb", "REAL"),
            ("disk_free_gb", "REAL"),
            ("load_avg_1m", "REAL"),
            ("load_avg_5m", "REAL"),
            ("load_avg_15m", "REAL"),
            ("process_count", "INTEGER"),
            ("predicted_availability", "REAL")
        ]
        
        for col_name, col_type in new_snap_cols:
            try:
                cursor.execute(f"ALTER TABLE snapshots ADD COLUMN {col_name} {col_type}")
                conn.commit()
                print(f"SUCCESS: La colonne dynamique '{col_name}' a été ajoutée.")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"INFO: La colonne dynamique '{col_name}' existe déjà.")
                else:
                    raise e
        
        # Also clean up old task tables if they still exist
        cursor.execute("DROP TABLE IF EXISTS task_results")
        cursor.execute("DROP TABLE IF EXISTS active_tasks")
        conn.commit()
        print("SUCCESS: Les anciennes tables de tâches ont été supprimées.")
        
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
