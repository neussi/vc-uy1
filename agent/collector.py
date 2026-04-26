import psutil
import datetime
import socket
import hashlib
import uuid
import platform
import re
import time

# --- PRIVACY & ETHICS (GLOBECOM 2023) ---
_buffer_cpu = []
_buffer_ram = []
_last_mac_anonymized = None

def get_mac_address(anonymize=True):
    """Retrieve MAC address with selective salted anonymization."""
    global _last_mac_anonymized
    if _last_mac_anonymized and anonymize:
        return _last_mac_anonymized
        
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    if anonymize:
        # Research salted hashing (selective anonymization)
        salt = "vc-uy1-cameroon-2026"
        hashed = hashlib.sha256((mac + salt).encode()).hexdigest()
        _last_mac_anonymized = hashed[:16] # Research-grade truncated ID
        return _last_mac_anonymized
    return mac

def get_stats(is_task_active=False, aggregate=True):
    """Collect system stats with optionally enabled local aggregation."""
    global _buffer_cpu, _buffer_ram
    
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    
    if aggregate:
        _buffer_cpu.append(cpu)
        _buffer_ram.append(ram)
        
        # Calculate averages for research-grade precision
        avg_cpu = sum(_buffer_cpu) / len(_buffer_cpu) if _buffer_cpu else cpu
        avg_ram = sum(_buffer_ram) / len(_buffer_ram) if _buffer_ram else ram
    else:
        avg_cpu = cpu
        avg_ram = ram

    try:
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged if battery else True
        percent = battery.percent if battery else 100
    except:
        plugged, percent = True, 100

    now = datetime.datetime.utcnow()
    local_now = datetime.datetime.now()

    return {
        "ts_utc": now.isoformat(),
        "ts_local": local_now.isoformat(),
        "day_of_week": local_now.weekday(),
        "hour_of_day": local_now.hour,
        "cpu": round(avg_cpu, 1),
        "ram": round(avg_ram, 1),
        "battery": percent,
        "plugged": plugged,
        "is_connected": check_connectivity(),
        "idle_seconds": get_idle_time(),
        "user_active": get_idle_time() < 300,
        "synthetic_task_active": is_task_active
    }

def check_connectivity(host="8.8.8.8", port=53, timeout=3):
    """Check if internet is available."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def get_idle_time():
    """Get idle time in seconds (simplified for demo)."""
    return 600 # Assume machine is idle for 10 mins for demo

def safe_to_run_task(idle_seconds: int) -> bool:
    """Check if it's safe to run a synthetic task."""
    SEUIL_CPU = 30
    SEUIL_RAM = 40
    IDLE_MIN_S = 300
    
    cpu_ok = psutil.cpu_percent(interval=1) < SEUIL_CPU
    ram_ok = psutil.virtual_memory().percent < SEUIL_RAM
    idle_ok = idle_seconds > IDLE_MIN_S
    return cpu_ok and ram_ok and idle_ok

def run_synthetic_task():
    """Simulate a computational task (dummy matrix multiplication)."""
    # This would be a separate thread in a full implementation
    pass
