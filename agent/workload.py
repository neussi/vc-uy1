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
    logger.info(f"Starting synthetic workload (Intensity: {intensity}) for {duration_s}s...")
    
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
    
    time.sleep(duration_s)
    
    for p in processes:
        if p.is_alive():
            p.terminate()
            
    end_time = datetime.datetime.utcnow()
    # Post-task stats
    cpu_after = psutil.cpu_percent()
    ram_after = psutil.virtual_memory().percent
    
    logger.info("Synthetic workload completed.")
    
    return {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "avg_cpu": (cpu_before + cpu_after) / 2,
        "avg_ram": (ram_before + ram_after) / 2,
        "actual_duration": (end_time - start_time).total_seconds(),
        "interrupted": False # Can be improved by checking if process was term'd early
    }

def cpu_stress(duration):
    """Busy loop for CPU stress."""
    start_time = time.time()
    while time.time() - start_time < duration:
        _ = 1234 * 5678 # Dummy op
