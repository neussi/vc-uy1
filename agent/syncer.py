import requests
import logging
import json
import collector
import datetime
import os
import sys
import certifi
import socket
import time
import psutil
import platform

def check_connectivity():
    """Proxy to collector connectivity check."""
    return collector.check_connectivity()

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

def get_cpu_model():
    """Retrieve clean, human-readable CPU model string."""
    if platform.system().lower() == "windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            val, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            return val.strip()
        except:
            return platform.processor() or "Unknown CPU"
    else:
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":", 1)[1].strip()
        except:
            pass
    return platform.processor() or "Unknown CPU"

def register(machine_id, consent_level=3):
    """Register machine with specific research consent level and volunteer preferences."""
    url = f"{SERVER_URL}/register"
    
    allowed_days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    allowed_slots = ["00:00-23:59"]
    contrib_mode = "total"
    
    pref_file = "preferences.json"
    if os.path.exists(pref_file):
        try:
            with open(pref_file, "r") as f:
                prefs = json.load(f)
                allowed_days = prefs.get("allowed_days", allowed_days)
                allowed_slots = prefs.get("allowed_slots", allowed_slots)
                contrib_mode = prefs.get("mode") or prefs.get("contrib_mode", contrib_mode)
        except Exception as e:
            logger.error(f"Error reading preferences for registration: {e}")

    try:
        disk_total = round(psutil.disk_usage('/').total / (1024**3), 1)
    except:
        disk_total = 0.0

    data = {
        "machine_id": machine_id,
        "hostname": socket.gethostname(),
        "os": platform.system().lower(),
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 1),
        "cpu_cores": psutil.cpu_count(),
        "timezone": time.tzname[0],
        "city": "Unknown",
        "consent_level": consent_level,
        "allowed_days": allowed_days,
        "allowed_slots": allowed_slots,
        "contrib_mode": contrib_mode,
        "cpu_model": get_cpu_model(),
        "cpu_cores_physical": psutil.cpu_count(logical=False) or psutil.cpu_count() or 1,
        "disk_total_gb": disk_total
    }
    try:
        requests.post(url, json=data, verify=get_verify_path(), timeout=10)
        logger.info(f"Registered with consent level {consent_level} and user preferences.")
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
