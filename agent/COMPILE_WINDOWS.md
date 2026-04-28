# Compilation de l'Agent VC-UY1 pour Windows (V3.1)

Pour garantir la persistance "Indestructible" (Service Système), suivez ces étapes sur une machine Windows 10 ou 11.

## 1. Pré-requis
- **Python 3.10+** (Ajoutez-le au PATH lors de l'installation).
- **Pip** (Installé par défaut avec Python).

## 2. Installation des Dépendances
Ouvrez un terminal (PowerShell ou CMD) dans le dossier `agent/` et exécutez :
```powershell
pip install pyinstaller psutil requests
```

## 3. Compilation du Binaire (.exe)
Exécutez la commande suivante pour générer l'exécutable final :
```powershell
pyinstaller --onefile --noconsole --name vc-agent-windows --icon NONE main.py
```
*Note : `--noconsole` permet à l'agent de tourner en arrière-plan sans ouvrir de fenêtre noire.*

## 4. Résultats
L'exécutable se trouvera dans le dossier `agent/dist/vc-agent-windows.exe`.

## 5. Déploiement Vital
- Copiez ce fichier sur les machines cibles.
- **IMPORTANT** : Faites un **clic-droit** -> **"Exécuter en tant qu'administrateur"**.
- C'est cette action unique qui permet à l'agent de s'enregistrer comme **Service Système** indétectable.

---
Laboratoire de Recherche VC-UY1 - Frugal Distributed Computing.
