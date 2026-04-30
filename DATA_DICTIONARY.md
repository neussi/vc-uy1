# 📖 Dictionnaire des Données : Dataset de Recherche VC-UY1

Toutes ces données sont effectivement collectées par l'agent et disponibles dans vos exports (**SQL, Excel, CSV, TXT**).

## 1. Table : `machines` (Identification du Nœud)
| Champ | Description | Intérêt Scientifique |
| :--- | :--- | :--- |
| `machine_id` | Identifiant unique (Hash SHA-256 de la MAC) | Anonymisation et suivi longitudinal. |
| `os` | Système d'exploitation (Windows/Linux) | Étude de la performance inter-OS. |
| `hostname_hash` | Hash du nom de la machine | Distinction des machines au sein d'un même réseau. |
| `cpu_cores` | Nombre de cœurs CPU | Capacité de calcul théorique. |
| `ram_total_mb` | RAM totale installée | Limite de charge mémoire. |
| `timezone` | Fuseau horaire (ex: Africa/Douala) | Corrélation avec les habitudes locales. |
| `registered_at` | Date d'inscription | Date d'entrée du volontaire dans le cluster. |

## 2. Table : `sessions` (Cycle de Disponibilité)
| Champ | Description | Intérêt Scientifique |
| :--- | :--- | :--- |
| `session_id` | UUID de la session actuelle | Regroupement des snapshots par période d'allumage. |
| `boot_time` | Heure du dernier démarrage système | Analyse de la persistance. |
| `shutdown_type` | 'clean' (extinction propre) ou 'power_cut' | Détection des arrêts brutaux. |
| `uptime_seconds`| Durée totale de la session | Fiabilité temporelle de la machine. |

## 3. Table : `snapshots` (Télémétrie Fine - Toutes les 5 min)
| Champ | Description | Intérêt Scientifique |
| :--- | :--- | :--- |
| `ts_utc / ts_local`| Horodatage précis (UTC et Local) | Analyse temporelle des usages. |
| `day_of_week` | Jour de la semaine (0-6) | Détection des cycles hebdomadaires. |
| `hour_of_day` | Heure locale (0-23) | Courbe de charge circadienne. |
| **Ressources** | | |
| `cpu_percent` | Utilisation instantanée du CPU (%) | Disponibilité de calcul résiduelle. |
| `cpu_freq_mhz` | Fréquence réelle du CPU | Détection du "throttling" thermique. |
| `ram_percent_used`| Utilisation de la RAM (%) | Capacité d'accueil de tâches lourdes. |
| **Énergie** | | |
| `battery_percent` | Niveau de batterie (%) | Autonomie des nœuds mobiles. |
| `power_plugged` | Branché sur secteur (Vrai/Faux) | Étabilité de la source d'énergie. |
| **Connectivité** | | |
| `network_latency_ms`| Latence vers le serveur central | Qualité de l'infrastructure réseau. |
| `bytes_sent_kb`    | Données envoyées (Float KB)     | Coût réseau du volontariat. |
| `bytes_recv_kb`    | Données reçues (Float KB)      | Coût réseau du volontariat. |
| **Activité** | | |
| `idle_seconds` | Temps depuis la dernière action user | Opportunité de calcul en arrière-plan. |
| `user_active` | Utilisateur actif (Vrai/Faux) | Priorité d'ordonnancement. |
| **Research Flag** | | |
| `synthetic_task_active`| Charge de test en cours | Marquage des données sous stress induit. |

## 4. Table : `power_events` (Analyse Électrique)
| Champ | Description | Intérêt Scientifique |
| :--- | :--- | :--- |
| `detected_at` | Moment de la détection de coupure | Chronologie des pannes de réseau. |
| `gap_seconds` | Durée estimée de l'arrêt | Sévérité de la coupure de courant. |
| `last_heartbeat_ts`| Dernier signe de vie reçu | Précision temporelle de l'incident. |

## 5. Table : `task_results` (Traces d'Exécution Fictives)
| Champ | Description | Intérêt Scientifique |
| :--- | :--- | :--- |
| `task_id` | Identifiant unique de la tâche | Suivi individuel des "jobs" distribués. |
| `start_time` | Heure de début de la tâche | Début de la période de disponibilité active. |
| `end_time` | Heure de fin (réelle) | Fin de la tâche. |
| `target_duration_s` | Durée prévue | Benchmark de performance. |
| `actual_duration_s` | Durée réelle exécutée | Analyse du décalage (overhead). |
| `interrupted` | Tâche interrompue (Vrai/Faux) | Corrélation avec le retour de l'utilisateur. |
| `avg_cpu_load` | Charge CPU moyenne pendant le job | Footprint de calcul de la tâche. |
| `avg_ram_load` | Charge RAM moyenne pendant le job | Footprint mémoire de la tâche. |
| `network_io_mb` | Volume réseau généré (MB) | Tracé de l'activité E/S (I/O). |

---
**En résumé :** Ce dataset vous donne la "vérité terrain" nécessaire pour entraîner vos modèles de prédiction de disponibilité.
