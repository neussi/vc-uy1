import time
import sys
import uuid
import heartbeat, collector, syncer, persistence, workload
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VC-Agent")

def main():
    logger.info("Starting VC-Agent...")
    
    # 0. Ensure persistence (Auto-start)
    persistence.ensure_persistence()
    
    # 1. Startup check for power cut
    status = heartbeat.detect_power_cut()
    if status and status['type'] == 'power_cut':
        logger.warning(f"Power cut detected! Downtime: {status['gap_s']}s")
        # In a real app, send this to the server immediately
    
    # 2. Register once and start session
    machine_id = collector.get_machine_id()
    session_id = str(uuid.uuid4())
    syncer.register(machine_id)
    syncer.start_session(machine_id, session_id)
    
    # 3. Main collection loop
    try:
        while True:
            stats = collector.get_stats()
            logger.info(f"Collected stats: CPU {stats['cpu_percent']}%")
            
            # Save heartbeat
            heartbeat.write_heartbeat()
            
            # Sync with server
            if stats['is_connected']:
                syncer.sync_batch(machine_id, session_id, [stats])
            
            # 4. Conditional workload trigger (for research data)
            if collector.safe_to_run_task(stats['idle_seconds']):
                # Run a small workload randomly (e.g. 10% chance per cycle)
                if time.time() % 10 < 1: # Simplified "random" for demo
                    workload.run_synthetic_workload(duration_s=15)

            time.sleep(20) # 20 seconds for live demo verification
    except KeyboardInterrupt:
        logger.info("Shutting down cleanly...")
        heartbeat.write_heartbeat(shutdown_clean=True)

if __name__ == "__main__":
    main()
