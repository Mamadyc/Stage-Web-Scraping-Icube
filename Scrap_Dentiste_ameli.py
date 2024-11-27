
from selenium import webdriver
from selenium.webdriver.common.by import By9
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 

# Créer une instance du navigateur Chrome
#driver = webdriver.Chrome(executable_path=chrome_driver_path)
path="/Users/mac/Desktop/chromedriver"
service= Service(executable_path=path)
driver = webdriver.Chrome(service=service)
# Ouvrir Google Maps
driver.get("https://annuairesante.ameli.fr/trouver-un-professionnel-de-sante/chirurgiens-dentistes/68-haut-rhin-mulhouse")

# Attendre que la page se charge
time.sleep(2)
noms_dentistes = []
adresses_dentistes = []
while True:
    # Recherche de tous les éléments contenant les noms des dentistes sur la page actuelle
    nom_dentists = driver.find_elements(By.CLASS_NAME, 'nom_pictos')
    adress = driver.find_elements(By.CLASS_NAME, 'item.left.adresse')
    
    
    # Impression des noms des dentistes sur la page actuelle
    for dentist,adress in zip( nom_dentists,adress):
        
        noms_dentistes.append(dentist.text)
        adresses_dentistes.append(adress.text)
    
    # Recherche de l'élément correspondant à la page suivante
    try:
        page_suivante = driver.find_element(By.XPATH, '//a[./img[contains(@alt, "Page suivante")]]')
        
        # Si l'élément de la page suivante est trouvé, cliquez dessus pour passer à la page suivante
        page_suivante.click()
        
        # Attente de quelques secondes pour que la nouvelle page se charge complètement
        time.sleep(2)
    except NoSuchElementException:
        # Si l'élément de la page suivante n'est pas trouvé, cela signifie que nous sommes arrivés à la dernière page
        break
    
df = pd.DataFrame({
    "Nom du dentiste": noms_dentistes,
    "Adresse du dentiste": adresses_dentistes
})

# Enregistrement du DataFrame dans un fichier CSV
df.to_csv("dentistes_mulhouse.csv", index=False)

    


    