import requests
import logging
import json
import collector
import datetime
import os
import sys
import certifi

# Fix for PyInstaller one-file bundled execution certificate resolution
if getattr(sys, 'frozen', False):
    # This ensures requests finds the CA bundle inside the temp MEI directory
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

logger = logging.getLogger("VC-Syncer")

SERVER_URL = "https://vc-uy1.npe-techs.com"

def get_verify_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'certifi', 'cacert.pem')
    return certifi.where()

def register(machine_id):
    """Register the machine with the server if not already done."""
    try:
        data = {
            "machine_id": machine_id,
            "os": "linux", # Should detect dynamically
            "hostname_hash": collector.get_machine_id(), # Sample
            "cpu_cores": 4, # Sample
            "ram_total_mb": 8192,
        }
        response = requests.post(f"{SERVER_URL}/register", json=data, timeout=10, verify=get_verify_path())
        return response.status_code in [200, 201]
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        return False

def start_session(machine_id, session_id):
    """Notify the server about a new session start."""
    try:
        data = {
            "session_id": session_id,
            "machine_id": machine_id,
            "boot_time": datetime.datetime.utcnow().isoformat(),
        }
        response = requests.post(f"{SERVER_URL}/sessions/start", json=data, timeout=10, verify=get_verify_path())
        return response.status_code in [200, 201]
    except Exception as e:
        logger.error(f"Session start failed: {e}")
        return False

def report_power_event(machine_id, event_type, gap_s):
    """Report a power cut or restoration event to the server."""
    payload = {
        "machine_id": machine_id,
        "event_type": event_type,
        "gap_s": gap_s,
        "ts_utc": datetime.datetime.utcnow().isoformat()
    }
    try:
        requests.post(f"{SERVER_URL}/sync/power-events", json=payload, timeout=10, verify=get_verify_path())
    except Exception as e:
        logger.error(f"Failed to report power event: {e}")

def report_task_result(task_data):
    """Report a synthetic task execution result to the server."""
    try:
        requests.post(f"{SERVER_URL}/sync/tasks", json=task_data, timeout=10, verify=get_verify_path())
    except Exception as e:
        logger.error(f"Failed to report task result: {e}")

def sync_batch(machine_id, session_id, snapshots):
    """Send a batch of snapshots to the server."""
    try:
        # Pre-process snapshots to ensure ISO format is strings and session_id is included
        for s in snapshots:
            s['session_id'] = session_id

        payload = {
            "machine_id": machine_id,
            "snapshots": snapshots
        }
        response = requests.post(f"{SERVER_URL}/sync/snapshots", json=payload, timeout=15, verify=get_verify_path())
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        return False
