# Scrapping

Ce code a pour objectif de scrapper les informations de produits sur un site e-commerce en utilisant Python. Il utilise les bibliothèques `requests` et `beautifulsoup` pour faire les requêtes HTTP et parser le HTML, `csv` pour écrire les données dans un fichier CSV et `termcolor` pour ajouter des couleurs à la sortie console.

## Creer un environement virtuel

Ouvrez un terminal (sur Linux ou Mac) ou une invite de commande (sur Windows) dans le dossier racine de votre projet.

Installez la bibliothèque "virtualenv" en utilisant la commande suivante : ```pip install virtualenv``` 

Créez un nouvel environnement virtuel en utilisant la commande suivante : ```virtualenv venv``` (**venv** c'est le nom de l'environnement, libre à vous de changer le nom)

Activez votre environnement virtuel en utilisant la commande suivante : ```source nom_de_votre_environnement/bin/activate```

Lorsque vous avez terminé de travailler sur votre projet, vous pouvez désactiver votre environnement virtuel en utilisant la commande suivante : ```deactivate```

## Installation
**Pour ce projet, j'utilise la version de Python 3.11.1.**
Toutes les librairies utilisées sont renseignées dans le fichier **requirements.txt**

Pour l'installation, lancer la commande ```pip install -r requirements.txt```

## Utilisation

Pour lancer le script, utiliser la commande ``` py script_scrapper.py ```, puis laissez vous guider par le programme
