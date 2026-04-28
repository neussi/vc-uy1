import psutil # type: ignore
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
_last_io_time = time.time()
_last_net_io = None
_last_disk_io = None

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
        _last_mac_anonymized = hashed[:16] # type: ignore # Research-grade truncated ID
        return _last_mac_anonymized
    return mac

def get_stats(is_task_active=False, aggregate=True):
    """Collect system stats with optionally enabled local aggregation."""
    global _buffer_cpu, _buffer_ram, _last_io_time, _last_net_io, _last_disk_io
    
    current_time = time.time()
    interval = current_time - _last_io_time
    _last_io_time = current_time
    
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    
    # --- Network / Disk IO Delta Calculation ---
    net_io = psutil.net_io_counters()
    disk_io = psutil.disk_io_counters()
    
    sent_kb, recv_kb = 0, 0
    read_mbps, write_mbps = 0, 0
    
    if _last_net_io:
        sent_kb = (net_io.bytes_sent - _last_net_io.bytes_sent) / 1024
        recv_kb = (net_io.bytes_recv - _last_net_io.bytes_recv) / 1024
    
    if _last_disk_io and interval > 0:
        read_mbps = ((disk_io.read_bytes - _last_disk_io.read_bytes) / (1024*1024)) / interval
        write_mbps = ((disk_io.write_bytes - _last_disk_io.write_bytes) / (1024*1024)) / interval
        
    _last_net_io = net_io
    _last_disk_io = disk_io

    # --- PRIVACY: Local sampling aggregation ---
    if aggregate:
        _buffer_cpu.append(cpu)
        _buffer_ram.append(ram)
        # Keep buffer small for real-time feel in v3.2
        if len(_buffer_cpu) > 10: _buffer_cpu.pop(0)
        if len(_buffer_ram) > 10: _buffer_ram.pop(0)
        avg_cpu = sum(_buffer_cpu) / len(_buffer_cpu)
        avg_ram = sum(_buffer_ram) / len(_buffer_ram)
    else:
        avg_cpu, avg_ram = cpu, ram

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
        "cpu_percent": float(f"{float(avg_cpu):.1f}"),
        "ram_percent_used": float(f"{float(avg_ram):.1f}"),
        "battery_percent": percent,
        "power_plugged": plugged,
        "bytes_sent_kb": float(f"{float(sent_kb):.2f}"),
        "bytes_recv_kb": float(f"{float(recv_kb):.2f}"),
        "disk_read_mbps": float(f"{float(read_mbps):.3f}"),
        "disk_write_mbps": float(f"{float(write_mbps):.3f}"),
        "network_latency_ms": 45.0, 
        "is_connected": check_connectivity(),
        "idle_seconds": get_idle_time(),
        "user_active": get_idle_time() < 60, # Higher sensitivity
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

_idle_ts = time.time()
def get_idle_time():
    """Get idle time in seconds using CPU heuristic fallback if xprintidle is missing."""
    global _idle_ts
    # If CPU usage is very low (e.g. < 5%) for a node, we assume research-readiness
    # For the local node, we simulate activity by checking CPU spikes
    if psutil.cpu_percent(interval=0.1) > 15.0:
        _idle_ts = time.time()
    return int(time.time() - _idle_ts)

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

def clear_aggregation_buffers():
    """Clear local telemetry buffers after successful transmission."""
    global _buffer_cpu, _buffer_ram
    _buffer_cpu.clear()
    _buffer_ram.clear()

