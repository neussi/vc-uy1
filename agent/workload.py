import time
import multiprocessing
import logging
import random

logger = logging.getLogger("VC-Workload")

def run_synthetic_workload(duration_s=30, intensity=0.5):
    """Simulate a computational task to collect data under load."""
    logger.info(f"Starting synthetic workload (Intensity: {intensity}) for {duration_s}s...")
    
    processes = []
    num_cores = multiprocessing.cpu_count()
    # Use a portion of cores based on intensity
    active_cores = max(1, int(num_cores * intensity))
    
    for _ in range(active_cores):
        p = multiprocessing.Process(target=cpu_stress, args=(duration_s,))
        p.start()
        processes.append(p)
        
    # Simulate RAM usage
    dummy_data = bytearray(int(100 * 1024 * 1024 * intensity)) # ~100MB * intensity
    
    time.sleep(duration_s)
    
    for p in processes:
        if p.is_alive():
            p.terminate()
            
    logger.info("Synthetic workload completed.")

def cpu_stress(duration):
    """Busy loop for CPU stress."""
    start_time = time.time()
    while time.time() - start_time < duration:
        _ = 1234 * 5678 # Dummy op
