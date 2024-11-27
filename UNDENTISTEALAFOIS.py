from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
# Créer une instance du navigateur Chrome
#driver = webdriver.Chrome(executable_path=chrome_driver_path)
df = pd.read_csv("C:\Users\conde\Desktop\Stage M1 2023-2024\comment_dentist_Alsace.csv")


path="/Users/mac/Desktop/chromedriver"
service= Service(executable_path=path)
driver = webdriver.Chrome(service=service)
# Ouvrir Google Maps
driver.get("https://www.google.fr/maps/@46.1106885,2.5911028,6z?entry=ttu")

# Attendre que la page se charge
time.sleep(1)

# Accepter les cookies
cookies_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span')
cookies_button.click()
time.sleep(1)

dentists = df['Nom du dentiste']
adresses = df['Adresse du dentiste']
df_final = pd.DataFrame(columns=["name", "star", "review", "response"])
for dentist,adress in zip(dentists,adresses):
    driver.get("https://www.google.fr/maps/@46.1106885,2.5911028,6z?entry=ttu")

# Attendre que la page se charge
    time.sleep(1)

# Accepter les cookies

    


# Rechercher les dentistes en Alsace
    search_box = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
    search_box.send_keys(dentist+" "+adress)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    check_review = True
    while check_review :
        try :
            review_tab = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]')
            review_tab.click()
            time.sleep(3)
            reviews = driver.find_elements(By.CLASS_NAME, 'wiI7pd')
            check_review = False
        except Exception :
            print("Can't find review_tab")
            break

        time.sleep(2)

    
    for _ in range (300):

        try: 
            scrollable_div = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

            scrollable_div.send_keys(Keys.END)
        
            reviews= driver.find_elements(By.CLASS_NAME,'m6QErb')
            for review in reviews : 
                try : 
                    afficher_plus  = driver.find_element(By.XPATH, './/button[@class="w8nwRe kyuRq" and contains(@aria-label, "more")]')
                    afficher_plus.click()
                

                except Exception : 
                    pass

        except Exception : 
            print("can't scroll")
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
# find value with critiria and collect to variable
    

    review_all = soup.find_all('span',{'class': 'wiI7pd'})
    

    response_all = soup.find_all('div', {'class': 'wiI7pd'})
    star_all = soup.find_all('span',{'class':'kvMYJc'})
    name_all = soup.find_all('div',{'class':'d4r55'})

    list_aria_label = []
    for star_test in star_all:
        aria_label = star_test.get('aria-label')
        list_aria_label.append(aria_label)


    response = []
    review = []
    star = []
    name = []





    for index, (stars, names) in enumerate(zip(star_all, name_all)):
        star_value = stars.get('aria-label')
        name_value = names.text
    
    # Si l'index dépasse la longueur de la liste des commentaires, cela signifie que le commentaire est vide
        if index < len(review_all):
            review_value = review_all[index].text
        else:
            review_value = ""  # Pour les commentaires vides, nous ajoutons une chaîne vide

        if index < len(response_all)  :

        
    
    

    
            response_value= response_all[index].text

        else : 
            response_value = ""
    
        review.append(review_value)
        response.append(response_value)
        star.append(star_value)
        
        



    df1 = pd.DataFrame({ 
                   
                            "name" : dentist,
                            "star": star, 
                            "review ": review ,
                            'response': response, })
    df_final = pd.concat([df_final, df1], ignore_index=True)
    
else : 
    driver.quit()
                   





    

    

# Enregistrer la DataFrame finale dans un fichier CSV
df_final.to_csv("fauteuilbleureview2.csv", index=False)       
                