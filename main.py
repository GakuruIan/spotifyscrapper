from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd

try:
    chrome_driver_path = "C:\\Users\\Administrator\\Downloads\\chromedriver-win64\\chromedriver.exe"

    website = "https://open.spotify.com/playlist/37i9dQZF1DWWWXigQZAD8B"

    # options=webdriver.ChromeOptions()
    # options.add_argument('--headless')
   

    services = Service(executable_path=chrome_driver_path)

    driver = webdriver.Chrome(service=services)
    driver.get(website)

    # wait for the rows to load completely
    wait = WebDriverWait(driver=driver,timeout=60)
    
    # get all the song rows
    rows = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class = 'contentSpacing']/div[@role='grid']/div[2]/div[2]/div[@role='row']")))

    artists =[]
    song_names = []
    songs_length=[]

    for row in rows:
         try:
            artist = row.find_element(by='xpath',value="./div[1]/div[2]/div[1]/span").text
            songname=row.find_element(by='xpath',value="./div[1]/div[3]/span/a").text
            songlen = row.find_element(by='xpath',value="./div[1]/div[5]/div").text
            
            if artist == 'E':
                artist = row.find_element(by='xpath',value="./div[1]/div[2]/div[1]/span[2]").text

            artists.append(artist)
            song_names.append(songname)  
            songs_length.append(songlen)

         except Exception as e:
            print(f"An error occurred in processing a row {e}")

    my_dict = {'song':song_names,'artist':artists,'length':songs_length}

    songlist=pd.DataFrame(my_dict)
    songlist.to_csv('topsongs.csv')

except TimeoutException as e:
    print(f"Error timeout exception {e}")

except WebDriverException as e:
    print(f"WebDriverException: {e}")
 

except Exception as e:
    print(f"An unexpected exception occurred: {e}")


finally :
    if driver:
        driver.quit()