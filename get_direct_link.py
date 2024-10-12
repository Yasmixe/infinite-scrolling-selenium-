from selenium import webdriver
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
from selenium.webdriver.chrome.service import Service

# Initialisation du WebDriver (assurez-vous que le bon driver est installé)
s = Service("C:/Users/DELL/Desktop/webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=s)

# Lire les liens depuis le fichier
with open("company_links.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]  # Récupérer chaque URL et retirer les espaces

# Fichier pour enregistrer les nouveaux liens extraits
output_file = open("extracted_links.txt", "w")

# Parcourir chaque lien
for url in urls:
    # Ouvrir le lien avec Selenium
    driver.get(url)
    
    # Attendre un peu pour que la page se charge complètement (ajuster si nécessaire)
    time.sleep(2)

    # Créer l'objet BeautifulSoup à partir de la page source actuelle
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Chercher une balise ou classe précise (exemple : chercher une balise avec une classe spécifique)
    for a_tag in soup.find_all("a", class_="mb-2 whitespace-nowrap md:mb-0"):
        if a_tag and 'href' in a_tag.attrs:  # Vérifier que l'attribut 'href' existe
            link = a_tag['href']
            full_url = urljoin(url, link)  # Construire l'URL complète si nécessaire
            output_file.write(full_url + "\n")  # Écrire l'URL dans le fichier texte
            print(full_url)  # Afficher l'URL extrait

# Fermer le fichier et le WebDriver
output_file.close()
driver.quit()
