import psutil
import datetime
import socket
import hashlib
import uuid

def get_machine_id():
    """Generate an anonymous ID based on MAC address."""
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
    return hashlib.sha256(mac.encode()).hexdigest()

def get_stats():
    """Collect current system metrics aligned with DB schema."""
    now = datetime.datetime.utcnow()
    local_now = datetime.datetime.now()
    
    # Battery/Power
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged if battery else True
    percent = battery.percent if battery else 100
    
    return {
        "ts_utc": now.isoformat(),
        "ts_local": local_now.isoformat(),
        "day_of_week": local_now.weekday(),
        "hour_of_day": local_now.hour,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_freq_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else 0,
        "ram_available_mb": psutil.virtual_memory().available // (1024 * 1024),
        "ram_percent_used": psutil.virtual_memory().percent,
        "power_plugged": plugged,
        "battery_percent": percent,
        "is_connected": check_connectivity(),
        "idle_seconds": get_idle_time(),
        "user_active": get_idle_time() < 300,
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
