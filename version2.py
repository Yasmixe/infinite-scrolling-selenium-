from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import json

# Initialiser le driver
s = Service("C:/Users/DELL/Desktop/webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=s)

# Liste de mots-clés pour les documents légaux
legal_keywords = ["legal", "terms", "condition", "policy", "privacy", "use", "disclaimer"]

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

                        # Vérifier si le lien ou le contenu contient l'un des mots-clés légaux
                        if any(keyword in link.lower() or keyword in content.lower() for keyword in legal_keywords):
                            # Ajouter le lien et le contenu dans le dictionnaire
                            site_data['links'].append({'link': link, 'content': content})

                # Écrire les données dans le fichier JSON immédiatement si des liens légaux sont trouvés
                if site_data['links']:
                    json.dump(site_data, json_file, ensure_ascii=False, indent=4)
                    json_file.write(",\n")  # Ajouter une virgule pour séparer les objets
            else:
                print(f"No footer found for {url}")

        except Exception as e:
            print(f"Error accessing {url}: {e}")

# Fermer le WebDriver
driver.quit()
