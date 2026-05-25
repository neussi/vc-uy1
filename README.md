# 🇨🇲 VC-UY1 : Plateforme de Télémétrie & Prédiction de Disponibilité pour le Calcul Volontaire

> **Master 2 Recherche Informatique — Université de Yaoundé I**  
> **Option** : Systèmes et Réseaux  
> **Directeur de Mémoire** : Dr. ADAMOU HAMZA  
> **Auteur** : Projet de Recherche et d'Implémentation de Calcul Volontaire (UY1)

---

## 🗺️ Cartographie Globale des Fichiers (Qui fait quoi ?)

Pour vous y retrouver instantanément, voici la liste des fichiers essentiels du projet et leurs rôles précis :

### 📡 1. Le Dossier de l'Agent Local (`/agent`)
Cet agent s'exécute en arrière-plan sur les ordinateurs des volontaires pour monitorer et prédire la disponibilité.
* **[agent/main.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/agent/main.py)** : Le point d'entrée principal. Gère l'installation interactive, configure les préférences de l'utilisateur (jours, heures de calcul) et lance la boucle de collecte d'arrière-plan.
* **[agent/collector.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/agent/collector.py)** : Récupère les métriques système (CPU, RAM, Swap, stockage, batterie, inactivité de l'utilisateur, état réseau).
* **[agent/predictor.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/agent/predictor.py)** : **Nouveau cœur prédictif.** Implémente le modèle linéaire **ARX résolu par Régression Ridge** et gère le buffer glissant de 72 heures.
* **[agent/syncer.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/agent/syncer.py)** : Gère les appels API sécurisés pour enregistrer la machine et synchroniser les snapshots en ligne.
* **[agent/persistence.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/agent/persistence.py)** : Assure la persistance de l'agent (redémarrage automatique sous Linux avec Systemd).
* **[agent/heartbeat.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/agent/heartbeat.py)** : Détecteur matériel de pannes et délestages électriques (mesure le gap de temps au redémarrage).

### 🛢️ 2. Le Dossier du Serveur Central (`/server`)
Reçoit les données de télémétrie et gère le portail de recherche.
* **[server/main.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/server/main.py)** : L'API FastAPI du serveur. Reçoit les snapshots des agents, expose les endpoints d'inscription et de monitoring.
* **[server/models.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/server/models.py)** : Définition des tables de la base de données SQLite/PostgreSQL via SQLAlchemy (`Machine`, `Snapshot`, `PowerEvent`).
* **[server/migrate_db.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/server/migrate_db.py)** : Script de migration de base de données (gère l'ajout à chaud des nouvelles colonnes de télémétrie).
* **[server/export.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/server/export.py)** : Moteur d'exportation dynamique des données en formats CSV, XLSX, JSON et dumps SQL pour l'entraînement des modèles.

### 🔬 3. Le Laboratoire d'Entraînement des Modèles (`/research_models`)
Un espace de recherche dédié pour entraîner, évaluer et comparer les performances des modèles séparément avant intégration.
* **[download_boinc_fta.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/download_boinc_fta.py)** : Télécharge et simule les traces globales du Failure Trace Archive (BOINC/SETI@home) pour le pré-entraînement.
* **[copy_local_data.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/copy_local_data.py)** : Prépare et structure les traces locales de Yaoundé (UY1) avec les délestages camerounais pour le fine-tuning.
* **[linear_model/train_linear_ridge.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/linear_model/train_linear_ridge.py)** : Entraîne et évalue le modèle **ARX avec Régression Ridge (L2)** sur les deux jeux de données (99.54% de précision locale !).
* **[gru_model/train_transfer_gru.py](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/research_models/gru_model/train_transfer_gru.py)** : Effectue le **Transfer Learning** du GRU (Pré-entraînement BOINC -> Fine-Tuning UY1) et démontre mathématiquement l'efficacité de la régularisation **EWC** contre l'oubli catastrophique.

### 📊 4. Le Dossier de Présentation (`/machine_monitoring`)
* **[presentation_donnees.tex](file:///home/npe-tech/Documents/M2 Recherche/vc-uy1/machine_monitoring/presentation_donnees.tex)** : Code source de votre présentation LaTeX Beamer pour votre professeur.
* **`*.bson` / `*.npy`** : Les jeux de données de télémétrie bruts et prétraités pour l'analyse locale.

---

## 🌟 L'Architecture Prédictive en 3 Piliers

L'architecture générale de VC-UY1 s'articule autour de 3 piliers scientifiques fondamentaux pour répondre aux défis des pays en développement :

### 📡 Pilier 1 : Télémétrie Frugale (Collecte Réelle)
Surveillance matérielle fine à une fréquence de **60 secondes**, mesurant la charge CPU, RAM, l'activité de l'utilisateur, l'état du réseau WiFi et la source d'alimentation (CA/Batterie), générant le premier jeu de données réel sur l'instabilité électrique des nœuds académiques à Yaoundé.

### 📈 Pilier 2 : Baseline Linéaire (ARX - Ridge L2)
* **Modèle** : Autoregressif avec Entrées Exogènes (ARX).
* **Entraînement** : Résolution globale périodique (toutes les 72h) par **Régression Ridge (L2)** sur le buffer local des 4320 snapshots.
* **Pourquoi ?** : La pénalité Ridge ($\alpha I$) immunise le modèle contre les corrélations de variables et assure la résilience mathématique complète (matrices toujours inversibles) face aux grands trous de données induits par les délestages.

### 🧠 Pilier 3 : Modèle Profond (GRU - Continual Learning EWC)
* **Modèle** : Réseau de neurones récurrents GRU pré-entraîné mondialement (Transfer Learning BOINC) et ajusté périodiquement (toutes les 24h).
* **Pourquoi ?** : Gère les patterns de présence non-linéaires complexes. Protégé contre l'**oubli catastrophique (Catastrophic Forgetting)** grâce à la régularisation **EWC** (*Elastic Weight Consolidation*).

---

## 🚀 Guide de Démarrage Rapide

### 1. Démarrer le Serveur Central (API)
Pour lancer le serveur FastAPI sur le port 6123 :
```bash
chmod +x start_server.sh
./start_server.sh
```

### 2. Lancer l'Agent sur un PC Volontaire (Linux)
Pour installer et configurer interactivement l'agent local :
```bash
python3 agent/main.py --setup
```
Pour le faire tourner en arrière-plan :
```bash
python3 agent/main.py
```

### 🔐 Identifiants d'Administration du Portail
* **Nom d'utilisateur** : `admin`
* **Mot de passe** : `vc-uy1-recherche`
