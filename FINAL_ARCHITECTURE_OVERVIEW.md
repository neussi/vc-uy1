# 🌍 VC-UY1 : Architecture du Système de Recherche de Volontariat Computing

Ce système a été conçu comme une plateforme de grade recherche pour permettre à l'Université de Yaoundé 1 de collecter des données longitudinales sur le Cloud Computing distribué en Afrique. Voici une explication complète de son fonctionnement et de ses composants.

## 1. Philosophie du Système
L'objectif est d'utiliser la puissance inutilisée des ordinateurs personnels (volontaires) pour créer un "Supercalculateur Virtuel". Pour votre recherche, le système se concentre sur la **caractérisation des ressources** : comprendre quand et comment les machines sont disponibles, leur puissance réelle sous charge, et leur fiabilité.

## 2. Architecture Technique (Le Triangle d'Or)

### A. L'Agent (Le Sondeur Furtif)
C'est le logiciel que les volontaires installent. 
- **Mode Démon (Stealth)** : Une fois lancé, il s'efface de l'écran et travaille en arrière-plan sans déranger l'utilisateur.
- **Persistance** : Il s'inscrit dans le système (systemd sur Linux, Registre sur Windows) pour se relancer automatiquement à chaque démarrage de l'ordinateur.
- **Collecte de Télémétrie** : Toutes les 5 minutes, il capture un instantané (snapshot) :
    - Utilisation CPU et Fréquence réelle.
    - Utilisation RAM.
    - État de la Batterie et Alimentation (pour détecter les coupures de courant).
    - Temps d'inactivité (Idle time).
- **Moteur de Charge Synthétique** : Il peut simuler des calculs intensifs pour tester comment la machine réagit sous pression.

### B. Le Serveur Central (Le Cerveau)
Déployé sur votre VPS, c'est le point de ralliement de tous les agents.
- **API REST (FastAPI)** : Gère les milliers de connexions entrantes avec une latence minimale.
- **Gestionnaire de Sessions** : Suit chaque machine de manière unique (UUID) pour calculer la durée de vie des sessions et la stabilité du réseau.
- **Base de Données Relationnelle** : Stocke chaque snapshot avec une précision à la milliseconde, alignée sur un schéma optimisé pour l'exportation scientifique.

### C. Le Dashboard Admin (Le Centre de Commandement)
Une interface web ultra-premium et responsive.
- **Visualisation Temps Réel** : Utilise **Recharts** pour dessiner les courbes d'utilisation CPU/RAM en direct.
- **Analyse de Topologie** : Vous montre la répartition des OS (Linux vs Windows) et la santé globale du cluster (Total Nodes, Uti/Sync efficiency).
- **Moteur d'Exportation Scientifique** : Permet de générer instantanément des jeux de données aux formats **SQL, Excel, CSV ou TXT** pour vos analyses statistiques ultérieures (R, Python, SPSS).

## 3. Infrastructure de Grade Production
- **Sécurité SSL/HTTPS** : Toutes les communications entre les agents et le serveur sont cryptées.
- **Reverse Proxy Apache** : Assure une haute disponibilité et une gestion propre des ports.
- **Pipeline CI/CD (GitHub Actions)** : Le système se met à jour automatiquement de manière sécurisée et résiliente.

## 4. Ce que nous avons accompli
Nous avons transformé un concept théorique en un outil de recherche **concret, déployé et robuste** :
1. **Passage au Temps Réel** : Les données ne sont plus statiques mais streamées en direct.
2. **Professionnalisation de l'Agent** : D'un simple script à un service système persistant et furtif.
3. **Flexibilité des Données** : Un système capable de fournir des rapports dans n'importe quel format académique standard.
4. **UX de Master** : Une interface moderne qui valorise votre travail lors de la soutenance.

---
**En résumé :** Vous disposez maintenant d'un réseau de capteurs distribués capables de fournir des données précises pour votre thèse pendant les 3 prochains mois, le tout piloté depuis un cockpit unique.
