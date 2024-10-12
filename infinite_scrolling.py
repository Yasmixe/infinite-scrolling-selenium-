import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium.webdriver.chrome.service import Service
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

##### Web scrapper for infinite scrolling page #####
s = Service("C:/Users/DELL/Desktop/webscraping/chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get("https://www.ycombinator.com/companies/")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break 

##### Extract Reddit URLs #####
urls = []
soup = BeautifulSoup(driver.page_source, "html.parser")
nb = 0 
# Rechercher toutes les balises <a> ayant la classe '_company_86jzd_338'
for a_tag in soup.find_all("a", class_="_company_86jzd_338"):
    if a_tag is not None and 'href' in a_tag.attrs:  # Vérifier que 'a_tag' existe et possède un 'href'
        base = "https://www.ycombinator.com"
        link = a_tag.attrs['href']
        url = urljoin(base, link)  # Construire l'URL complète
        urls.append(url)  # Ajouter l'URL à la liste
        print(url)  # Afficher l'URL
        nb = nb+ 1

print(nb)
