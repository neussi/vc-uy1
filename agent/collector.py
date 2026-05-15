import psutil # type: ignore
import datetime
import socket
import hashlib
import uuid
import platform
import re
import time
import math
import json
import os
from collections import deque

# --- RESEARCH SPECIFICATIONS (18 DIMENSIONS) ---
HISTORY_FILE = "collector_history.json"
PREFERENCES_FILE = "preferences.json"

class FeatureEngine:
    def __init__(self):
        self.cpu_history = deque(maxlen=1440) # 24 hours at 60s/sample
        self.last_outage_ts = time.time()
        self.load_history()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    data = json.load(f)
                    self.cpu_history = deque(data.get("cpu_history", []), maxlen=1440)
                    self.last_outage_ts = data.get("last_outage_ts", time.time())
            except: pass

    def save_history(self):
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump({
                    "cpu_history": list(self.cpu_history),
                    "last_outage_ts": self.last_outage_ts
                }, f)
        except: pass

    def get_cyclic_time(self, val, period):
        sin_val = math.sin(2 * math.pi * val / period)
        cos_val = math.cos(2 * math.pi * val / period)
        return sin_val, cos_val

    def get_moving_stats(self):
        # Dim 9-11: Moving Averages (1h, 6h, 24h)
        # Dim 12: Std Dev (1h)
        history_list = list(self.cpu_history)
        avg_1h = sum(history_list[-60:]) / len(history_list[-60:]) if history_list else 0
        avg_6h = sum(history_list[-360:]) / len(history_list[-360:]) if history_list else 0
        avg_24h = sum(history_list) / len(history_list) if history_list else 0
        
        # Std Dev 1h
        if len(history_list[-60:]) > 1:
            mean = avg_1h
            variance = sum((x - mean) ** 2 for x in history_list[-60:]) / len(history_list[-60:])
            std_1h = math.sqrt(variance)
        else:
            std_1h = 0
            
        return avg_1h, avg_6h, avg_24h, std_1h

    def get_outage_stats(self):
        # Dim 16: Hours since last outage log(1+x)
        hours_since = (time.time() - self.last_outage_ts) / 3600
        log_hours = math.log1p(hours_since)
        
        # Dim 17: Outage in progress (Fusion logic)
        outage_in_progress = 0
        try:
            battery = psutil.sensors_battery()
            if battery and not battery.power_plugged:
                outage_in_progress = 1
        except: pass
        
        return log_hours, outage_in_progress

    def get_compatibility_score(self, local_now):
        # Dim 18: User preference score
        if not os.path.exists(PREFERENCES_FILE):
            return 1.0 # Default to fully available if no prefs
            
        try:
            with open(PREFERENCES_FILE, "r") as f:
                prefs = json.load(f)
                
            day_name = local_now.strftime("%a").lower() # e.g. "mon"
            current_time = local_now.time()
            
            # Check if current day is allowed
            allowed_days = prefs.get("allowed_days", [])
            if allowed_days and day_name not in allowed_days:
                return 0.0
                
            # Check if current time is within allowed slots
            allowed_slots = prefs.get("allowed_slots", [])
            if not allowed_slots:
                return 1.0
                
            for slot in allowed_slots:
                start_str, end_str = slot.split("-")
                start_time = datetime.datetime.strptime(start_str, "%H:%M").time()
                end_time = datetime.datetime.strptime(end_str, "%H:%M").time()
                
                if start_time <= current_time <= end_time:
                    return 1.0
                # Handle overnight slots (e.g. 22:00-06:00)
                if start_time > end_time:
                    if current_time >= start_time or current_time <= end_time:
                        return 1.0
            return 0.0
        except:
            return 1.0

engine = FeatureEngine()

def get_mac_address(anonymize=True):
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    if anonymize:
        salt = "vc-uy1-cameroon-2026"
        return hashlib.sha256((mac + salt).encode()).hexdigest()[:16]
    return mac

def get_stats(aggregate=True):
    global engine
    
    # 1. Base Metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_free_mb = ram.available / (1024 * 1024)
    
    # Update history
    engine.cpu_history.append(cpu_percent)
    engine.save_history()
    
    now = datetime.datetime.utcnow()
    local_now = datetime.datetime.now()
    
    # 2. Generate 18-Dimension Feature Vector
    # Dim 1-8: Cyclic Time
    s_hour, c_hour = engine.get_cyclic_time(local_now.hour, 24)
    s_dow, c_dow = engine.get_cyclic_time(local_now.weekday(), 7)
    s_dom, c_dom = engine.get_cyclic_time(local_now.day, 31)
    s_mon, c_mon = engine.get_cyclic_time(local_now.month, 12)
    
    # Dim 9-12: Moving Stats
    avg1, avg6, avg24, std1 = engine.get_moving_stats()
    
    # Dim 13-15: System State
    cpu_free = 100.0 - cpu_percent
    is_conn = 1 if check_connectivity() else 0
    
    # Dim 16-17: Outage
    log_h, outage_active = engine.get_outage_stats()
    
    # Dim 18: Preferences
    compat_score = engine.get_compatibility_score(local_now)
    
    # 3. Build Result
    return {
        "ts_utc": now.isoformat(),
        "ts_local": local_now.isoformat(),
        
        # --- THE 18 DIMENSIONS ---
        "features": [
            s_hour, c_hour, s_dow, c_dow, s_dom, c_dom, s_mon, c_mon, # 1-8
            avg1, avg6, avg24, std1,                                 # 9-12
            cpu_free, ram_free_mb, is_conn,                          # 13-15
            log_h, outage_active,                                    # 16-17
            compat_score                                             # 18
        ],
        
        # --- RAW METRICS FOR DASHBOARD ---
        "cpu_percent": cpu_percent,
        "ram_percent_used": ram.percent,
        "is_connected": is_conn == 1,
        "power_plugged": outage_active == 0,
        "idle_seconds": get_idle_time()
    }

def check_connectivity(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

_idle_ts = time.time()
def get_idle_time():
    global _idle_ts
    if psutil.cpu_percent(interval=0.1) > 15.0:
        _idle_ts = time.time()
    return int(time.time() - _idle_ts)

def clear_aggregation_buffers():
    pass # No longer needed with new history engine
