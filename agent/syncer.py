import requests
import logging
import json
from . import collector, database # Assuming I'll need a local DB later, but for now just send directly

logger = logging.getLogger("VC-Syncer")

SERVER_URL = "http://vc-uy1.npe-techs.com" # Should be configurable

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
        response = requests.post(f"{SERVER_URL}/register", json=data, timeout=10)
        return response.status_code in [200, 201]
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        return False

def sync_batch(machine_id, snapshots):
    """Send a batch of snapshots to the server."""
    try:
        payload = {
            "machine_id": machine_id,
            "snapshots": snapshots
        }
        response = requests.post(f"{SERVER_URL}/sync/snapshots", json=payload, timeout=15)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        return False
