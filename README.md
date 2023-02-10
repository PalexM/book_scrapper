# Scrapping de produits en utilisant Python 

Ce code a pour objectif de scrapper les informations de produits sur un site e-commerce en utilisant Python. Il utilise les bibliothèques `requests` et `beautifulsoup` pour faire les requêtes HTTP et parser le HTML, `csv` pour écrire les données dans un fichier CSV et `termcolor` pour ajouter des couleurs à la sortie console.

## Phase 1 

La fonction `scrapProductInformations` prend en entrée une URL de produit et extrait les informations suivantes :

- URL de la page produit 
- Code universel du produit 
- Titre du produit 
- Prix incluant la taxe 
- Prix excluant la taxe 
- Nombre disponible 
- Description du produit 
- Catégorie 
- Note de l'avis 
- URL de l'image 

En cas d'erreur de connexion ou de statut, un message d'erreur est affiché en rouge à la console.

## Phase 2 

La fonction `scrapCategories` extrait les titres et les liens des catégories disponibles sur le site e-commerce.

La fonction `scrapPageByCategory` prend en entrée un lien de catégorie et extrait les liens de chaque produit sur la page. Elle boucle à travers toutes les pages jusqu'à ce qu'il n'y ait plus de pages à parcourir.

## Stockage des données 

Les informations extraites sont stockées dans un fichier CSV en utilisant la fonction `writeCsv`. Les entêtes du fichier CSV sont définies dans la fonction.

