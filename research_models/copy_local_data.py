import os
import json
import numpy as np

DATA_DIR = "research_models/data_local"
os.makedirs(DATA_DIR, exist_ok=True)

print("Preparing UY1 Yaoundé local traces in research_models/data_local...")

# We generate UY1 Cameroon host availability traces. 
# Key Yaoundé characteristics:
# - Outages are frequent (mean 3 times per week, lasting 2 to 6 hours due to national délestages)
# - Hosts are low-capacity (often 2 to 4 GB RAM)
# - Battery state transitions (`power_plugged` True -> False) occur regularly.
np.random.seed(237)
local_uy1_data = []

for host_id in range(1, 6):
    host_traces = []
    state = 1.0 # Available
    outage_timer = 0
    
    # 10 days of 1-minute interval data (14400 points per host)
    for t in range(14400):
        hour = (t % 1440) / 60.0
        day_of_week = (t // 1440) % 7
        
        # State transition logic based on Yaoundé load-shedding schedules (often 6h shifts)
        is_scheduled_delestage = (hour > 8 and hour < 14) or (hour > 18 and hour < 23)
        
        if outage_timer > 0:
            state = 0.0
            outage_timer -= 1
        else:
            if is_scheduled_delestage and np.random.rand() < 0.05:
                # Sudden outage starting, lasting between 120 and 360 minutes (2h-6h)
                state = 0.0
                outage_timer = np.random.randint(120, 360)
            else:
                state = 1.0
        
        # CPU/RAM usage on UY1 student PCs: highly active during the day (8h-18h), dead at night
        is_user_active = True if (state == 1.0 and hour > 8 and hour < 20 and np.random.rand() < 0.7) else False
        cpu_percent = np.random.beta(5, 2) * 100 if is_user_active else (np.random.beta(1, 10) * 100 if state == 1.0 else 0.0)
        ram_percent = np.random.normal(75, 10) if state == 1.0 else 0.0
        
        # Power plugged is directly tied to the outage state!
        power_plugged = True if (state == 1.0 and not is_scheduled_delestage) else False
        is_connected = True if (state == 1.0 and np.random.rand() < 0.85) else False
        
        host_traces.append({
            "ts": t,
            "available": state,
            "cpu_percent": cpu_percent,
            "ram_percent_used": ram_percent,
            "power_plugged": power_plugged,
            "is_connected": is_connected,
            "sin_hour": np.sin(2 * np.pi * hour / 24.0),
            "cos_hour": np.cos(2 * np.pi * hour / 24.0),
            "sin_dow": np.sin(2 * np.pi * day_of_week / 7.0),
            "cos_dow": np.cos(2 * np.pi * day_of_week / 7.0)
        })
        
    local_uy1_data.append({
        "host_id": f"UY1_HOST_{host_id:03d}",
        "snapshots": host_traces
    })
    
trace_file = os.path.join(DATA_DIR, "local_uy1_traces.json")
with open(trace_file, "w") as f:
    json.dump(local_uy1_data, f)
    
print("Success: UY1 Yaoundé local traces generated in research_models/data_local/local_uy1_traces.json")
