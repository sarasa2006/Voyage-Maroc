@echo on
cd /d "%~dp0"

echo ==============================================
echo       Lancement de Projet Voyage
echo ==============================================

echo Activation de l'environnement virtuel...
call backend\.venv\Scripts\activate.bat

echo Demarrage du serveur Django...
cd backend
python manage.py runserver

pause
