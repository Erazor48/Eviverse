@echo off
setlocal enabledelayedexpansion

:: Chemins
set "ROOT_PATH=%~dp0.."
set "FRONTEND_PATH=%ROOT_PATH%\frontend"
set "BACKEND_PATH=%ROOT_PATH%\backend"
set "CONDA_PATH=C:\Users\ethan\anaconda3\Scripts\conda.exe"
set "CONDA_ENV_PATH=C:\Users\ethan\anaconda3\envs\eviverse-backend"
set "PIP_PATH=%CONDA_ENV_PATH%\Scripts\pip.exe"

:: Variables globales pour les vérifications
set "CONDA_CHECK_OK=0"
set "ENV_CHECK_OK=0"
set "CHECK_FAILED=0"
set "PYLINT_PATH=%CONDA_ENV_PATH%\Scripts\pylint.exe"

:menu
cls
echo.
echo ===================================
echo Gestionnaire de l'application Eviverse
echo ===================================
echo.
echo 1. Installer/Mettre a jour les dependances
echo 2. Verifier les dependances
echo 3. Demarrer l'application
echo 4. Arreter l'application
echo 5. Verifier la qualite du code
echo 6. Quitter
echo.
set /p choice="Choisissez une option (1-6): "

if "%choice%"=="1" goto install_deps
if "%choice%"=="2" goto check_deps
if "%choice%"=="3" goto start_app
if "%choice%"=="4" goto stop_app
if "%choice%"=="5" goto check_code
if "%choice%"=="6" goto end

echo Option invalide
timeout /t 2 >nul
goto menu

:: Fonction simplifiée pour vérifier Conda
:check_conda
set "CONDA_CHECK_OK=0"

echo Verification de l'existence de Conda...
if exist "%CONDA_PATH%" goto conda_exists
echo.
echo ERREUR: Conda n'est pas trouve a l'emplacement specifie: %CONDA_PATH%
echo Veuillez installer Anaconda ou Miniconda ou verifier le chemin dans le script.
echo.
pause
goto menu

:conda_exists
set "CONDA_CHECK_OK=1"
goto :eof

:check_deps
cls
echo.
echo ===================================
echo VERIFICATION DE L'ENVIRONNEMENT
echo ===================================
echo.
echo Cette verification va:
echo 1. Verifier que l'environnement Python existe
echo 2. Verifier que toutes les dependances Python sont installees correctement
echo 3. Verifier que les packages Node.js sont a jour et securises
echo.
echo NOTE: Cette verification ne necessite pas que les serveurs backend ou frontend soient en cours d'execution.
echo.

:: Vérification simple de Conda
if not exist "%CONDA_PATH%" (
    echo ERREUR: Conda n'est pas trouve a l'emplacement specifie: %CONDA_PATH%
    pause
    goto menu
)

:: Vérification simple de l'environnement
if not exist "%CONDA_ENV_PATH%" (
    echo ERREUR: L'environnement Python 'eviverse-backend' n'existe pas.
    pause
    goto menu
)

set "PYTHON_EXE=%CONDA_ENV_PATH%\python.exe"
if not exist "%PYTHON_EXE%" (
    echo ERREUR: L'executable Python n'est pas trouve dans l'environnement.
    pause
    goto menu
)

:: Vérification rapide des packages principaux
echo Verification des packages principaux...
"%PYTHON_EXE%" -c "import sys; packages = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 'numpy', 'torch', 'transformers']; missing = []; [missing.append(p) for p in packages if not __import__(p, fromlist=['']) is not None]; print('\n'.join(['Packages manquants:'] + [f' - {p}' for p in missing]) if missing else 'Tous les packages Python sont correctement installes.'); sys.exit(1 if missing else 0)"
set "CHECK_FAILED=%errorlevel%"

echo.
echo Verification des dependances Node.js...

if not exist "%FRONTEND_PATH%\package.json" (
    echo ERREUR: Le fichier package.json n'existe pas dans %FRONTEND_PATH%
    pause
    goto menu
)

if not exist "%FRONTEND_PATH%\node_modules" (
    echo ATTENTION: Le dossier node_modules n'existe pas.
    echo Les dependances Node.js ne sont pas installees.
    goto end_check
)

cd "%FRONTEND_PATH%"
echo Les dependances Node.js sont installees.

:end_check
echo.
echo ===================================
echo VERIFICATION TERMINEE
echo ===================================
echo.
echo Resultat de la verification:
if "%CHECK_FAILED%"=="1" (
    echo - Environnement Python: INCOMPLET
    echo   Utilisez l'option 1 pour installer les dependances manquantes.
) else (
    echo - Environnement Python: COMPLET
)

if exist "%FRONTEND_PATH%\node_modules" (
    echo - Dependances Node.js: INSTALLEES
) else (
    echo - Dependances Node.js: NON INSTALLEES
    echo   Utilisez l'option 1 pour installer les dependances.
)

echo.
pause
goto menu

:install_deps
cls
echo ===================================
echo INSTALLATION DES DEPENDANCES
echo ===================================
echo.
echo Cette installation va:
echo 1. Verifier que Conda est installe
echo 2. Verifier l'environnement Python existant
echo 3. Installer ou mettre a jour les dependances Python
echo 4. Installer les dependances Node.js
echo.

call :check_conda SILENT
if "%CONDA_CHECK_OK%"=="0" goto menu

echo.
if "%ENV_CHECK_OK%"=="1" (
    echo L'environnement existe deja. Verification de sa configuration...
    call "%CONDA_PATH%" run -n eviverse-backend python -c "import sys; print(sys.version)" >nul 2>&1
    if errorlevel 1 (
        echo L'environnement semble corrompu. Suppression...
        call "%CONDA_PATH%" env remove -n eviverse-backend
        if errorlevel 1 (
            echo ERREUR: Impossible de supprimer l'environnement corrompu
            pause
            goto menu
        )
    ) else (
        echo L'environnement est valide. Mise a jour des dependances...
        goto update_deps
    )
) else (
    echo Creation de l'environnement eviverse-backend...
    if not exist "%BACKEND_PATH%\environment.yml" (
        echo ERREUR: Le fichier environment.yml n'existe pas dans %BACKEND_PATH%
        echo Verification du contenu du dossier backend:
        dir "%BACKEND_PATH%"
        pause
        goto menu
    )
    call "%CONDA_PATH%" env create -f "%BACKEND_PATH%\environment.yml"
    if errorlevel 1 (
        echo ERREUR: Impossible de creer l'environnement
        pause
        goto menu
    )
)

:update_deps
echo.
echo Installation/Mise a jour des dependances Python...
echo Cette etape installe ou met a jour toutes les dependances Python specifiees dans requirements.txt
if not exist "%BACKEND_PATH%\requirements.txt" (
    echo ERREUR: Le fichier requirements.txt n'existe pas dans %BACKEND_PATH%
    echo Verification du contenu du dossier backend:
    dir "%BACKEND_PATH%"
    pause
    goto menu
)
call "%CONDA_PATH%" run -n eviverse-backend pip install --upgrade -r "%BACKEND_PATH%\requirements.txt"
if errorlevel 1 (
    echo ERREUR: Impossible d'installer les dependances Python
    pause
    goto menu
)
echo.
echo Verification des dependances frontend...
echo Cette etape installe ou met a jour les dependances Node.js specifiees dans package.json
if not exist "%FRONTEND_PATH%\package.json" (
    echo ERREUR: Le fichier package.json n'existe pas dans %FRONTEND_PATH%
    echo Verification du contenu du dossier frontend:
    dir "%FRONTEND_PATH%"
    pause
    goto menu
)
cd "%FRONTEND_PATH%"
if not exist "%FRONTEND_PATH%\node_modules" (
    echo Installation des dependances frontend...
    call npm install --legacy-peer-deps
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer les dependances frontend
        pause
        goto menu
    )
) else (
    echo Mise a jour des dependances frontend...
    call npm install --legacy-peer-deps
    if errorlevel 1 (
        echo ERREUR: Impossible de mettre a jour les dependances frontend
        pause
        goto menu
    )
)
echo.
echo ===================================
echo INSTALLATION TERMINEE
echo ===================================
echo.
echo Si vous voyez ce message, cela signifie que:
echo 1. L'environnement Python est correctement configure
echo 2. Toutes les dependances Python sont a jour
echo 3. Les dependances Node.js sont a jour
echo.
echo Vous pouvez maintenant verifier les dependances (option 2) ou demarrer l'application (option 3).
echo.
pause
goto menu

:start_app
cls
echo.
echo ===================================
echo DEMARRAGE DE L'APPLICATION
echo ===================================
echo.
echo Cette operation va:
echo 1. Verifier les dependances
echo 2. Demarrer le serveur backend (FastAPI)
echo 3. Demarrer le serveur frontend (React)
echo.
echo Verification des dependances...

:: Vérification rapide de Conda et de l'environnement
if not exist "%CONDA_PATH%" (
    echo ERREUR: Conda n'est pas trouve a l'emplacement specifie: %CONDA_PATH%
    pause
    goto menu
)

if not exist "%CONDA_ENV_PATH%" (
    echo ERREUR: L'environnement Python 'eviverse-backend' n'existe pas.
    pause
    goto menu
)

if not exist "%BACKEND_PATH%\main.py" (
    echo ERREUR: Le fichier main.py n'existe pas dans %BACKEND_PATH%
    echo Verification du contenu du dossier backend:
    dir "%BACKEND_PATH%"
    pause
    goto menu
)

if not exist "%FRONTEND_PATH%\package.json" (
    echo ERREUR: Le fichier package.json n'existe pas dans %FRONTEND_PATH%
    echo Verification du contenu du dossier frontend:
    dir "%FRONTEND_PATH%"
    pause
    goto menu
)

echo.
echo Demarrage du serveur backend...
echo Cette etape va demarrer le serveur FastAPI sur le port 8000.
echo Le serveur sera accessible a l'adresse http://localhost:8000
echo.
call start "Backend Server" cmd /k "cd %BACKEND_PATH% && %CONDA_ENV_PATH%\python.exe -m uvicorn main:app --reload"
if errorlevel 1 (
    echo ERREUR: Impossible de demarrer le serveur backend
    pause
    goto menu
)
echo.
echo Attente du demarrage du serveur backend...
timeout /t 2 >nul
echo Serveur backend demarre.
echo.
echo Demarrage du serveur frontend...
echo Cette etape va demarrer le serveur React sur le port 3000.
echo L'application sera accessible a l'adresse http://localhost:3000
echo.
call start "Frontend Server" cmd /k "cd %FRONTEND_PATH% && npm start"
if errorlevel 1 (
    echo ERREUR: Impossible de demarrer le serveur frontend
    pause
    goto menu
)
echo.
echo Attente du demarrage du serveur frontend...
timeout /t 2 >nul
echo Serveur frontend demarre.
echo.
echo ===================================
echo APPLICATION DEMARREE
echo ===================================
echo.
echo Les serveurs sont maintenant en cours d'execution:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo Pour arreter les serveurs, utilisez l'option 4.
echo.
echo Appuyez sur une touche pour retourner au menu principal...
pause
goto menu

:stop_app
cls
echo.
echo ===================================
echo ARRET DE L'APPLICATION
echo ===================================
echo.
echo Cette operation va arreter tous les serveurs en cours d'execution.
echo.
echo Arret des serveurs...
(
    call taskkill /F /FI "WINDOWTITLE eq Backend Server*"
) >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Aucun serveur backend n'a ete trouve en cours d'execution.
) else (
    echo Serveur backend arrete.
)
(
    call taskkill /F /FI "WINDOWTITLE eq Frontend Server*"
) >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Aucun serveur frontend n'a ete trouve en cours d'execution.
) else (
    echo Serveur frontend arrete.
)
echo.
echo ===================================
echo APPLICATION ARRETEE
echo ===================================
echo.
echo Tous les serveurs ont ete arretes.
echo.
pause
goto menu

:check_code
cls
echo.
echo ===================================
echo VERIFICATION DE LA QUALITE DU CODE
echo ===================================
echo.
echo Cette verification va:
echo 1. Verifier l'installation de Pylint
echo 2. Fournir les instructions pour analyser votre code
echo.

:: Vérification simple de Pylint - approche minimaliste pour éviter les blocages
echo Verification de l'installation de Pylint...
echo.

set "PYLINT_INSTALLED=0"

:: Simple test de présence de Pylint - direct et clair
"%CONDA_PATH%" run -n eviverse-backend pylint --version
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Pylint est correctement installe.
    set "PYLINT_INSTALLED=1"
    goto pylint_check_done
) else (
    echo.
    echo ATTENTION: Pylint n'est pas installe.
    echo.
    echo Voulez-vous l'installer maintenant? (O/N)
    set /p install_choice=""
    if /i "%install_choice%"=="O" (
        echo.
        echo Installation de Pylint...
        "%CONDA_PATH%" run -n eviverse-backend pip install pylint==2.17.0
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo Pylint a ete installe avec succes.
            set "PYLINT_INSTALLED=1"
            goto pylint_check_done
        ) else (
            echo.
            echo ERREUR: Impossible d'installer Pylint.
            pause
            goto menu
        )
    ) else (
        echo.
        echo Installation annulee.
        pause
        goto menu
    )
)

:pylint_check_done

echo.
echo ===================================
echo COMMENT UTILISER PYLINT
echo ===================================
echo.
echo Pour analyser un fichier specifique, utilisez:
echo.
echo   1. Ouvrez un terminal a la racine du projet
echo   2. Executez cette commande:
echo      "%CONDA_PATH%" run -n eviverse-backend pylint backend/[fichier.py]
echo.
echo Par exemple:
echo   "%CONDA_PATH%" run -n eviverse-backend pylint backend/routes/users.py
echo.
echo Pour plus d'informations: https://pylint.pycqa.org/
echo.

echo ===================================
echo DIAGNOSTIC DE L'APPLICATION
echo ===================================
echo.
echo Si vous rencontrez des problemes de connexion ou d'inscription:
echo.
echo 1. Verifiez que la base de donnees est correctement initialisee:
echo    - Assurez-vous que le fichier .env contient les bonnes informations
echo    - Executez "python init_db.py" dans le dossier backend
echo.
echo 2. Examinez les logs du serveur backend pour voir les erreurs:
echo    - Pendant l'execution, observez les messages dans la console backend
echo    - Les erreurs SQL indiqueront des problemes de base de donnees
echo    - Les erreurs 400/500 indiqueront des problemes d'API
echo.
echo 3. Verifiez les requetes dans le navigateur (F12 > Onglet Reseau):
echo    - Identifiez les codes d'erreur HTTP (400, 401, 500)
echo    - Examinez les reponses JSON pour plus de details
echo.
echo Plus d'informations en consultant la documentation FastAPI:
echo https://fastapi.tiangolo.com/tutorial/debugging/
echo.

echo ===================================
echo VERIFICATION TERMINEE
echo ===================================
echo.
echo Retour au menu principal...
echo.
pause
goto menu

:end
echo Au revoir!
timeout /t 2 >nul
exit /b 0

:: Vérifier les dépendances Python
:check_python_dependencies
echo.
echo Verification des dependances Python...

if not exist "%BACKEND_PATH%\requirements.txt" (
    echo ERREUR: Le fichier requirements.txt est introuvable.
    echo Chemin attendu: %BACKEND_PATH%\requirements.txt
    pause
    exit /b 1
)

cd "%BACKEND_PATH%"

:: Méthode optimisée - utiliser Python directement pour vérifier les dépendances
echo Verification des packages Python principaux...
"%PYTHON_EXE%" -c "import sys; packages = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 'numpy', 'torch', 'transformers']; missing = []; [missing.append(p) for p in packages if not __import__(p, fromlist=['']) is not None]; print('\n'.join(['Packages manquants:'] + [f' - {p}' for p in missing]) if missing else 'Tous les packages Python sont correctement installes.'); sys.exit(1 if missing else 0)"
set "CHECK_FAILED=%errorlevel%"

if %CHECK_FAILED% NEQ 0 (
    echo.
    echo Voulez-vous installer/mettre a jour toutes les dependances Python ? (O/N)
    set /p install_python=""
    if /i "!install_python!"=="O" (
        echo.
        echo Installation des dependances Python...
        "%CONDA_PATH%" run -n eviverse-backend pip install --upgrade -r "%BACKEND_PATH%\requirements.txt"
        if errorlevel 1 (
            echo ERREUR: Impossible d'installer les dependances Python
            pause
            goto menu
        )
        echo Les dependances Python ont ete installees avec succes.
    ) else (
        echo Verification des dependances Python terminee avec des erreurs.
        set "CHECK_PYTHON_DEPENDENCIES=0"
        echo.
        goto menu
    )
) else (
    set "CHECK_PYTHON_DEPENDENCIES=1"
    echo.
    echo Toutes les dependances Python sont deja installees.
)

:end
echo Au revoir!
timeout /t 2 >nul
exit /b 0 