import time
import sys
import uuid
import heartbeat, collector, syncer, persistence
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
    
    level = 3 
    print(f"-> Niveau sélectionné par défaut pour la recherche : {level}")
    
    with open(consent_file, "w") as f:
        json.dump({"consent_level": level, "accepted_at": time.time()}, f)
    return level

def set_preferences():
    """Prompt for user availability preferences."""
    pref_file = "preferences.json"
    if os.path.exists(pref_file):
        return

    print("\n" + "="*60)
    print("   CONFIGURATIONS DE DISPONIBILITÉ (Recherche)")
    print("="*60)
    print("Souhaitez-vous limiter la collecte à certaines heures ?")
    print("Par défaut : 24h/24 (Optimal pour la précision du modèle)")
    print("Appuyez sur Entrée pour accepter, ou configurez plus tard dans preferences.json")
    print("="*60)
    
    # Default preferences
    prefs = {
        "allowed_days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
        "allowed_slots": ["00:00-23:59"]
    }
    
    with open(pref_file, "w") as f:
        json.dump(prefs, f, indent=4)
    print("-> Préférences enregistrées (24h/7j).")

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
    
    # 1. Interactive setup before backgrounding
    consent_level = get_consent()
    set_preferences()
    
    # 2. Backgrounding
    if "--foreground" not in sys.argv:
        daemonize()

    logger.info("Starting VC-Agent Daemon...")
    
    # 3. Ensure persistence (Auto-start)
    persistence.ensure_persistence()
    
    # 4. Startup check for power cut
    machine_id = collector.get_mac_address()
    status = heartbeat.detect_power_cut()
    if status and status['type'] == 'power_cut':
        logger.warning(f"Power cut detected! Downtime: {status['gap_s']}s")
        syncer.report_power_event(machine_id, "power_cut", status['gap_s'])
    
    # 5. Register and verify consent
    session_id = str(uuid.uuid4())
    syncer.register(machine_id, consent_level=consent_level)
    syncer.start_session(machine_id, session_id)
    
    # NEW: Immediate Startup Pulse (for instant visibility)
    logger.info("Sending initial startup pulse...")
    initial_stats = collector.get_stats(aggregate=False)
    syncer.sync_batch(machine_id, session_id, [initial_stats])
    
    # 5. Main collection loop (Privacy-Aware)
    # 5. Main collection loop (Privacy-Aware)
    last_power_status = None
    try:
        while True:
            # Phase 1: Local Aggregation (Micro-cycles of 60s)
            # We collect 5 mini-samples before sending the snapshot
            for _ in range(5):
                stats = collector.get_stats(aggregate=True)
                
                # Detect transition (Instant response)
                current_power_status = stats['power_plugged']
                if last_power_status is not None and current_power_status != last_power_status:
                    event_type = "to_ac" if current_power_status else "to_battery"
                    logger.info(f"Power transition: {event_type}")
                    syncer.report_power_event(machine_id, event_type, 0)
                last_power_status = current_power_status

                # Heartbeat logic check
                heartbeat.write_heartbeat()
                
                # Faster sampling for the demo (15s instead of 60s)
                time.sleep(15) 

            # Phase 2: Transmission (Aggregated data)
            if syncer.check_connectivity():
                # Get the aggregated stats (averages)
                final_stats = collector.get_stats(aggregate=True)
                syncer.sync_batch(machine_id, session_id, [final_stats])
                collector.clear_aggregation_buffers()
                logger.info("Aggregated snapshot synchronized.")
    except KeyboardInterrupt:
        logger.info("Shutting down cleanly...")
        heartbeat.write_heartbeat(shutdown_clean=True)

if __name__ == "__main__":
    main()
