# EVIverse - Environnement Virtuel Interactif

EVIverse est une plateforme qui permet de créer et manipuler des objets 3D à partir d'images, de texte et de modèles existants.

## 🚀 Démarrage rapide

### Prérequis
- Anaconda ou Miniconda (recommandé)
- Node.js et npm

### Installation et démarrage

1. Clonez le dépôt :
   ```
   git clone [URL du dépôt]
   cd [nom du dépôt]
   ```

2. Exécutez simplement le script `setup.bat` :
   ```
   setup.bat
   ```

Le script `setup.bat` est conçu pour fonctionner automatiquement :
- Il détecte votre installation Anaconda
- Crée ou utilise l'environnement "eviverse" existant
- Installe les dépendances nécessaires 
- Démarre directement l'application
- Ouvrez votre navigateur à l'adresse http://localhost:3000 pour accéder à l'application

## 🔧 Mode d'emploi des scripts

### demarrer.bat
Script de démarrage rapide qui lance directement l'application sans passer par les menus.

### setup.bat 
Centre de contrôle complet qui offre les fonctionnalités suivantes :
- **Démarrage** : Lance l'application avec l'environnement approprié
- **Configuration** : Permet d'installer toutes les dépendances
- **Diagnostic** : Outils pour résoudre les problèmes courants (CORS, ports, etc.)
- **Détection intelligente** : S'adapte à l'environnement Python disponible

## 📚 À propos du projet

EVIverse vous permet de :
- Créer des projets 3D
- Générer des objets 3D à partir d'images et de descriptions textuelles
- Manipuler ces objets dans un éditeur de scène
- Partager vos créations avec d'autres utilisateurs

## 🛠️ Structure du projet

```
├── eviverse/                     # Dossier principal de l'application
│   ├── backend/                  # API Backend (FastAPI)
│   │   ├── api/                  # Endpoints API
│   │   ├── core/                 # Fonctionnalités principales
│   │   ├── models/               # Modèles de base de données
│   │   └── schemas/              # Schémas de validation
│   ├── frontend/                 # Interface utilisateur (React)
│   │   ├── public/               # Fichiers statiques
│   │   └── src/                  # Code source React
│   │       ├── components/       # Composants réutilisables
│   │       ├── contexts/         # Contextes React (Auth, etc.)
│   │       └── pages/            # Pages de l'application
│   ├── media/                    # Fichiers médias générés
│   │   ├── storage/              # Stockage général
│   │   └── thumbnails/           # Miniatures des objets
│   ├── models/                   # Modèles d'IA
│   └── .env                      # Configuration d'environnement
│
├── scripts/                      # Scripts utilitaires additionnels
│   └── organize_project.bat      # Organisation du projet
│
├── docs/                         # Documentation supplémentaire
│
├── README.md                     # Documentation principale
├── setup.bat                     # Centre de contrôle principal
├── demarrer.bat                  # Script de démarrage rapide
└── .gitignore                    # Configuration Git
```

## 📦 Installation manuelle (Alternative)

Si vous préférez installer manuellement :

### Backend (Python)

```bash
cd eviverse
pip install -r requirements.txt
```

### Frontend (React)

```bash
cd eviverse/frontend
npm install
```

## 🏃‍♂️ Démarrage manuel (Alternative)

### Backend
```bash
cd eviverse
python -m backend.main
```

### Frontend
```bash
cd eviverse/frontend
npm start
```

## 🔍 Résolution des problèmes

### Problèmes de démarrage
- Si le backend ne démarre pas, vérifiez que Python est bien installé et que les dépendances sont installées
- Si le frontend ne démarre pas, vérifiez que Node.js est bien installé et que les dépendances sont installées

### Problème spécifique à Python sous Windows
Si vous voyez l'erreur "Python est introuvable ; exécutez sans arguments pour installer à partir du Microsoft Store...", voici les solutions :

1. **Solution automatique** : Le script `setup.bat` recherche maintenant Python de plusieurs façons :
   - Commande `python` standard
   - Python Launcher (`py`)
   - Emplacements d'installation courants
   - Environnement Anaconda

2. **Solution permanente** : 
   - Lors de l'installation de Python, cochez la case "Add Python to PATH"
   - Si Python est déjà installé, vous pouvez :
     - Réinstaller Python en cochant cette option
     - Ajouter manuellement Python à votre PATH système
     - Désactiver l'application "App Installer" dans Paramètres > Applications > Exécution d'applications

### Problèmes de CORS
Si vous rencontrez des erreurs CORS, utilisez l'option de diagnostic dans `setup.bat`.

### Autres problèmes
Consultez la documentation détaillée dans le dossier `docs/`

## 📜 Licence

Ce projet est sous licence MIT. 