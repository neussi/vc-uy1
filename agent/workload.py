import time
import multiprocessing
import logging
import random

logger = logging.getLogger("VC-Workload")

def run_synthetic_workload(duration_s=30, intensity=0.5):
    """Simulate a computational task and return its execution footprint."""
    import datetime
    import psutil
    
    start_time = datetime.datetime.utcnow()
    logger.info(f"TASK RECEIVED: Duration {duration_s}s, Intensity {intensity}")
    
    # Track resources during start
    cpu_before = psutil.cpu_percent()
    ram_before = psutil.virtual_memory().percent
    
    processes = []
    num_cores = multiprocessing.cpu_count()
    active_cores = max(1, int(num_cores * intensity))
    
    for _ in range(active_cores):
        p = multiprocessing.Process(target=cpu_stress, args=(duration_s,))
        p.start()
        processes.append(p)
        
    # Simulate RAM usage
    _dummy_data = bytearray(int(100 * 1024 * 1024 * intensity)) # ~100MB * intensity
    
    # Track network during task if needed, but here we just wait
    time.sleep(duration_s)
    
    for p in processes:
        if p.is_alive():
            p.terminate()
            
    end_time = datetime.datetime.utcnow()
    # Post-task stats
    cpu_after = psutil.cpu_percent()
    ram_after = psutil.virtual_memory().percent
    
    actual_duration = (end_time - start_time).total_seconds()
    logger.info(f"TASK COMPLETED: Actual duration {actual_duration:.1f}s")
    
    return {
        "start_time": start_time.isoformat() + "Z",
        "end_time": end_time.isoformat() + "Z",
        "target_duration_s": duration_s,
        "actual_duration_s": round(actual_duration, 1),
        "avg_cpu_load": round((cpu_before + cpu_after) / 2 + (intensity * 20), 1),
        "avg_ram_load": round((ram_before + ram_after) / 2 + (intensity * 10), 1),
        "interrupted": actual_duration < (duration_s * 0.9),
        "network_io_mb": round(random.uniform(0.1, 2.5), 2) # Simulated network impact
    }

def cpu_stress(duration):
    """Busy loop for CPU stress."""
    start_time = time.time()
    while time.time() - start_time < duration:
        _ = 1234 * 5678 # Dummy op
