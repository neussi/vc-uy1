import time
import sys
import uuid
import heartbeat, collector, syncer, persistence, workload
import logging
import os

# Configure logging to file for background execution
LOG_FILE = "agent_system.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=LOG_FILE,
    filemode='a'
)
logger = logging.getLogger("VC-Agent")

def print_welcome_message():
    """Display a professional terminal message to the user."""
    message = r"""
    ############################################################
    #                                                          #
    #   VC-UY1 : VOLUNTEER COMPUTING RESEARCH AGENT            #
    #                                                          #
    #   Installation terminée avec succès !                     #
    #                                                          #
    #   Tout se passera bien sans déranger votre machine.      #
    #   Nous allons juste collecter des données sur la charge  #
    #   de votre CPU et mémoire.                               #
    #                                                          #
    #   Merci de participer à l'évolution de la tech           #
    #   en Afrique par la recherche scientifique.              #
    #                                                          #
    ############################################################
    """
    print(message)
    print("\nL'agent fonctionne maintenant en arrière-plan. Vous pouvez fermer ce terminal.\n")

def daemonize():
    """Fork the process into the background (Linux)."""
    if os.name != 'posix':
        return # Windows backgrounding is handled differently (pythonw/registry)
    
    try:
        pid = os.fork()
        if pid > 0:
            # First parent exists
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork #1 failed: {e}")
        sys.exit(1)

    os.setsid()
    
    try:
        pid = os.fork()
        if pid > 0:
            # Second parent exists
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork #2 failed: {e}")
        sys.exit(1)

def main():
    # 0. Show welcome message
    print_welcome_message()
    
    # 1. Backgrounding
    if "--foreground" not in sys.argv:
        daemonize()

    logger.info("Starting VC-Agent Daemon...")
    
    # 2. Ensure persistence (Auto-start)
    persistence.ensure_persistence()
    
    # 3. Startup check for power cut
    status = heartbeat.detect_power_cut()
    if status and status['type'] == 'power_cut':
        logger.warning(f"Power cut detected! Downtime: {status['gap_s']}s")
    
    # 4. Register once and start session
    machine_id = collector.get_machine_id()
    session_id = str(uuid.uuid4())
    syncer.register(machine_id)
    syncer.start_session(machine_id, session_id)
    
    # 5. Main collection loop
    try:
        while True:
            stats = collector.get_stats()
            logger.info(f"Collected stats: CPU {stats['cpu_percent']}%")
            
            # Save heartbeat
            heartbeat.write_heartbeat()
            
            # Sync with server
            if stats['is_connected']:
                syncer.sync_batch(machine_id, session_id, [stats])
            
            # 6. Conditional workload trigger (for research data)
            if collector.safe_to_run_task(stats['idle_seconds']):
                # Run a small workload randomly (e.g. 10% chance per cycle)
                if time.time() % 30 < 1: 
                    workload.run_synthetic_workload(duration_s=15)

            time.sleep(300) # 5 minutes for pro research cycle
    except KeyboardInterrupt:
        logger.info("Shutting down cleanly...")
        heartbeat.write_heartbeat(shutdown_clean=True)

if __name__ == "__main__":
    main()
