from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from fpdf import FPDF
import PyPDF2
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json 
# initialiser le driver
s = Service("C:/Users/DELL/Desktop/webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=s)


# Lire les liens depuis le fichier
with open("extracted_links.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]  # Récupérer chaque URL et retirer les espaces

# Ouvrir le fichier JSON en mode écriture (ou création s'il n'existe pas encore)
with open("footer_data.json", "a", encoding='utf-8') as json_file:

    # Parcourir chaque lien
    for url in urls:
        try:
            # Ouvrir le lien avec Selenium
            driver.get(url)

            # Attendre un peu pour que la page se charge complètement
            time.sleep(5)

            # Créer l'objet BeautifulSoup à partir de la page source actuelle
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Chercher les balises <footer> et récupérer les liens et leur contenu texte
            footer = soup.find("footer")  # Trouver la balise <footer>
            if footer:  # Vérifier si la balise <footer> existe
                site_data = {'url': url, 'links': []}  # Dictionnaire pour stocker les liens et leur contenu pour ce site
                for a_tag in footer.find_all("a"):  # Rechercher toutes les balises <a> dans le footer
                    if a_tag and 'href' in a_tag.attrs:  # Vérifier que l'attribut 'href' existe
                        link = a_tag['href']
                        content = a_tag.get_text(strip=True)  # Extraire le texte associé au lien
                        # Ajouter le lien et le contenu dans le dictionnaire
                        site_data['links'].append({'link': link, 'content': content})

                # Écrire les données dans le fichier JSON immédiatement
                json.dump(site_data, json_file, ensure_ascii=False, indent=4)
                json_file.write(",\n")  # Ajouter une virgule pour séparer les objets
            else:
                print(f"No footer found for {url}")

        except Exception as e:
            print(f"Error accessing {url}: {e}")

# Fermer le WebDriver
driver.quit()