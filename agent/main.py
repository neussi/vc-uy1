import time
import sys
import uuid
import heartbeat, collector, syncer, persistence, workload
import logging
import os
import json
import argparse
import random

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

def get_consent():
    """Load or prompt for Research Consent Level (GLOBECOM 2023)."""
    consent_file = "consent.json"
    if os.path.exists(consent_file):
        try:
            with open(consent_file, "r") as f:
                return json.load(f).get("consent_level", 1)
        except:
            pass
            
    print("\n" + "="*60)
    print("   UNIVERSITY OF YAOUNDE 1 - RESEARCH CONSENT FRAMEWORK")
    print("="*60)
    print("Veuillez choisir votre niveau de partage de données :")
    print("1. Essentiel : Profil matériel, disponibilité de base")
    print("2. Système : Métriques de performance, patterns d'erreurs")
    print("3. Recherche : Modèles comportementaux anonymisés (Standard)")
    print("4. Feedback : Enquêtes d'expérience utilisateur")
    print("="*60)
    
    # In interactive mode, we could ask, but for large scale we default to 3
    # or look for an environment variable / cli arg.
    level = 3 
    print(f"-> Niveau sélectionné par défaut pour la recherche : {level}")
    
    with open(consent_file, "w") as f:
        json.dump({"consent_level": level, "accepted_at": time.time()}, f)
    return level

def daemonize():
    """Fork the process into the background (Linux/Posix only)."""
    if os.name != 'posix':
        return # Windows uses Registry/Startup for backgrounding (non-blocking)
    
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork #1 failed: {e}")
        sys.exit(1)

    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork #2 failed: {e}")
        sys.exit(1)
    
    # Detach standard file descriptors for full daemonization
    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'rb') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'ab') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open('/dev/null', 'ab') as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

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
    machine_id = collector.get_mac_address()
    status = heartbeat.detect_power_cut()
    if status and status['type'] == 'power_cut':
        logger.warning(f"Power cut detected! Downtime: {status['gap_s']}s")
        syncer.report_power_event(machine_id, "power_cut", status['gap_s'])
    
    # 4. Register and verify consent
    session_id = str(uuid.uuid4())
    consent_level = get_consent()
    syncer.register(machine_id, consent_level=consent_level)
    syncer.start_session(machine_id, session_id)
    
    # NEW: Immediate Startup Pulse (for instant visibility)
    logger.info("Sending initial startup pulse...")
    initial_stats = collector.get_stats(is_task_active=False, aggregate=False)
    syncer.sync_batch(machine_id, session_id, [initial_stats])
    
    # 5. Main collection loop (Privacy-Aware)
    is_workload_running = False
    last_power_status = None
    try:
        while True:
            # Phase 1: Local Aggregation (Micro-cycles of 60s)
            # We collect 5 mini-samples before sending the 5-min snapshot (GLOBECOM 2023)
            for _ in range(5):
                stats = collector.get_stats(is_task_active=is_workload_running, aggregate=True)
                
                # Detect transition (Instant response)
                current_power_status = stats['power_plugged']
                if last_power_status is not None and current_power_status != last_power_status:
                    event_type = "to_ac" if current_power_status else "to_battery"
                    logger.info(f"Power transition: {event_type}")
                    syncer.report_power_event(machine_id, event_type, 0)
                last_power_status = current_power_status

                # Heartbeat and Workload logic check
                heartbeat.write_heartbeat()
                
                # --- Workload Trigger (Research Node Intelligence) ---
                # ULTRA-LOW threshold for developer validation (30s instead of 300s)
                if not is_workload_running and collector.get_idle_time() >= 30:
                    # High probability for instant WOW effect
                    if random.random() < 0.8:
                        import threading
                        def run_and_track():
                            nonlocal is_workload_running
                            is_workload_running = True
                            task_id = str(uuid.uuid4())
                            # Intensity varied for statistical range
                            intensity = random.choice([0.3, 0.5])
                            # RESEARCH UPDATE: Duration now ranges from 1 hour to 2 hours
                            duration = random.randint(3600, 7200)
                            result = workload.run_synthetic_workload(duration_s=duration, intensity=intensity)
                            
                            # Attach identification
                            result.update({
                                "task_id": task_id,
                                "machine_id": machine_id,
                                "session_id": session_id
                            })
                            
                            # Log and sync task result
                            logger.info(f"Submitting RESEARCH TASK results: {task_id}")
                            syncer.report_task_result(result)
                            is_workload_running = False
                            
                        threading.Thread(target=run_and_track, daemon=True).start()

                # Faster sampling for the demo (15s instead of 60s)
                time.sleep(15) 

            # Phase 2: Transmission (Aggregated data)
            if syncer.check_connectivity():
                # Get the aggregated stats (averages)
                final_stats = collector.get_stats(is_task_active=is_workload_running, aggregate=True)
                syncer.sync_batch(machine_id, session_id, [final_stats])
                collector.clear_aggregation_buffers()
                logger.info("Aggregated snapshot synchronized (Privacy-Mode).")
    except KeyboardInterrupt:
        logger.info("Shutting down cleanly...")
        heartbeat.write_heartbeat(shutdown_clean=True)

if __name__ == "__main__":
    main()
