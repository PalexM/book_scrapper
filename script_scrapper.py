import requests
from bs4 import BeautifulSoup
import csv
import re
from termcolor import colored
import os
import pathlib

# PHASE 1 




def scrap_product_informations(url): 
    
    try:
        response = requests.get(url) # chager la page web
        soup = BeautifulSoup(response.content, 'html.parser')  # parser la page chargé
        response.raise_for_status() # verification de status de la page (200)
        product_page_url = url
        # Scrapper les differents informations de la page
        universal_product_code = soup.find_all("td")[0].string
        title = soup.find_all("h1")[0].string
        price_including_tax = soup.find_all("td")[2].string
        price_excluding_tax = soup.find_all("td")[3].string
        number_available = re.findall(r'\d+', soup.find_all("td")[5].string)[0] # garder que les ciffres
        product_description = soup.find_all("p")[3].string
        category = soup.find_all("a")[3].string
        review_rating = fonction_switch(soup.find('p', {'class': 'star-rating'}).get('class')[1])
        image_url = 'http://books.toscrape.com/' +soup.find_all("img")[0]['src'][6:]
        
        download_and_store_img(image_url, title) # telecharger et enregistrer l'image

        return [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url] 

    except requests.exceptions.HTTPError as error: # status different de 200 
        print(colored('Erreur de statut, veuillez vérifier le lien ou réessayer : \n '+ str(error), 'red'))

    except requests.exceptions.ConnectionError as error: # le serveur ne reponds pas
        print(colored('Impossible de se connecter au serveur, veuillez réessayer plus tard : \n '+ str(error), 'red'))

    except Exception as error: # autres erreurs
        print(colored('Url incorect : \n ' + str(error), 'red' ))

# ecrire les donnes dans un fichier CSV
def write_csv(data, category_name):
    headers = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description','category', 'review_rating', 'image_url'] #ENTETS CSV
    
    csv_folder = pathlib.Path.cwd().joinpath("csv")  # chemin d'enregistrement
    if not csv_folder.exists():
        csv_folder.mkdir()

    csv_file = csv_folder.joinpath(category_name + '.csv')
    with open(csv_file, 'w', encoding='UTF8', newline='') as file: # creer ou mettre a jour le fichier CSV
        writer = csv.writer(file)
        # ecrire les entetes 
        writer.writerow(headers)
        for inf in data:
            # ecrire les donnees 
            writer.writerow(inf)


# PHASE 2 

def scrap_categories():

    try:
        url = 'http://books.toscrape.com/index.html'
        response = requests.get(url) # chager la page web
        soup = BeautifulSoup(response.content, 'html.parser') # parser la page chargé
        categories = soup.select('#default > div > div > div > aside > div.side_categories > ul > li > ul > li > a') # scrapper les categories existants
        categories_title = [] 
        categories_link = [] 

        for element in categories:
            categories_title.append(element.string.strip()) # noms des cathegories
            categories_link.append('http://books.toscrape.com/' + element.get('href')[:-10]) # liens des cathegories
        
        return [categories_title,categories_link]

    except requests.exceptions.HTTPError as error: # status different de 200 
        print(colored('Erreur de statut, veuillez vérifier le lien ou réessayer : \n '+ str(error), 'red'))

    except requests.exceptions.ConnectionError as error: # le serveur ne reponds pas
        print(colored('Impossible de se connecter au serveur, veuillez réessayer plus tard : \n '+ str(error), 'red'))
   
    except Exception as error: # autres erreurs
        print(colored('Erreur : \n ' + str(error), 'red' ))


def scrap_page_by_category(url):

    loop = True
    index = 'index'
    i = 1 
    results = [] # tableau avec les liens de chaque element de la page
    while loop : # boucle sur toutes les pages de cette categorie
        if(requests.get(url + str(index) + '.html').status_code) != 404 : # verification si la page existe
            response = requests.get(url + str(index) + '.html') # chager la page 
            soup = BeautifulSoup(response.content, 'html.parser') # parser la page chargé
            category_name = soup.select('#default > div > div > div > div > div.page-header.action > h1')
            links = soup.select('#default > div > div > div > div > section > div:nth-child(2) > ol > li > article > h3 > a')
            for link in links:
                results.append(scrap_product_informations('http://books.toscrape.com/catalogue' + link.get('href')[8:]))
            i += 1
            index = 'page-' + str(i)
        else:
            loop = False
    category_name = re.sub(r'[^a-zA-Z0-9]', '', category_name[0].string) # retirer les espaces
    write_csv(results,category_name)

# phase 3

def select_category():
    options = scrap_categories()
    titles = options[0]
    links = options[1] 
    opt = ' \n' #la liste des options
    print(colored(' \n\t\t\t\t\t\t Veuillez choisir une catégorie','cyan'))
    for index, element in enumerate(titles):    
        while len(element) <= 20: #  égalisation des longueurs de texte pour l'esthétique et la mise en page
            element = element +' '

        if index % 5 == 4: # creer 5 colones pour la mise en page
            opt += colored(index,'blue') + ' : ' + colored(element,'white') + '\t\n'
        else:
            opt += colored(index,'blue') + ' : ' + colored(element,'white') + '\t'
    print(colored(opt,'cyan'))
    try:
        selected = int(input())
        try:
            select = links[selected] #verification que lien existe
            print(colored('Veuillez patienter, votre fichier est en cours de génération.','green'))
            scrap_page_by_category(select)
            print(colored('Le traitement a été effectué avec succès ! Les données ont été stockées dans le dossier CSV et les photos dans le dossier PHOTOS','green'))
        except IndexError:
            print("Le nombre entré ne correspond à aucune catégorie, veuillez réessayer.",'red')
            select_category()
    except ValueError:
        print("Seulement les nombres sont acceptés, veuillez réessayer.",'red')
        select_category()


# Scrapper tout les pages
def scrape_all():
    categories = scrap_categories()
    categories_links = categories[1]
    
    for link in categories_links:
         scrap_page_by_category(link)


# phase 4
# telecharger et enregistrer les images
def download_and_store_img(url, name):
    

    r = requests.get(url)
    text = re.sub(r'[^a-zA-Z0-9]', '', name)
    file_name = text + ".jpg"

    photos_folder = pathlib.Path.cwd().joinpath("photos") #chemin d'enregistrement
    if not photos_folder.exists():
        photos_folder.mkdir()

    file_path = photos_folder.joinpath(file_name)
    with open(file_path, "wb") as f:
        f.write(r.content)


def fonction_switch(arg):
    switch = {
        'Zero' : 0,
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    return switch.get(arg)



def main():

    print(colored('\n\t\t\t\t\t\t Veuillez choisir parmi les options suivantes : \n','cyan'))
    print(colored('\n\t\t 1. Scraper la page d\'un Bookin  \t\t 2. Scrap Une Cathegorie \t\t 3. Scrapper Tout','cyan'))
    select = input()

    if select == '1':
        url = input(colored('\n\t\t Veuillez entrer l\'URL : \n\t\t\t\t','cyan'))
        data = scrap_product_informations(url)
        print(colored('Veuillez patienter, votre fichier est en cours de génération.','green'))
        write_csv([data], re.sub(r'[^a-zA-Z0-9]', '', data[2]))
        print(colored('Le traitement a été effectué avec succès ! Les données ont été stockées dans le dossier CSV et les photos dans le dossier PHOTOS','green'))
    elif select == '2':
        select_category()
    elif select == '3':
        print(colored('Veuillez patienter, votre fichier est en cours de génération.','green'))
        scrape_all()
        print(colored('Le traitement a été effectué avec succès ! Les données ont été stockées dans le dossier CSV et les photos dans le dossier PHOTOS','green'))
    else :
        print(colored("Erreur de sélection, veuillez réessayer.",'red'))

if __name__ == "__main__": 
    main()
