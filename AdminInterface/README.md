# Fonctionnement :

## Setup

### Installation de l'environnment virtuel et des librairies :

virtualenv venv -p python3
source /venv/bin/activate
pip install -r requirements.txt

### Migration du schema vers les bases de données

python manage.py migrate

## Lancement du serveur

python manage.py runserver