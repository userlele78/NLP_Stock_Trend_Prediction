# Dataframe
import pandas as pd

# Web Crawling
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Other
import time
from tqdm import tqdm

def investing_com_crawl():
    news_data = []
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging


    link_website = "https://vn.investing.com/"
    driver = webdriver.Chrome(options = options)  # , service=service
    driver.get(link_website)
    time.sleep(5)


    # Find the search box
    seach_key_locating = driver.find_element(By.XPATH, '//*[@id="__next"]/header/div[1]/section/div[2]/div[1]/button')
    seach_key_locating.click()

    search_box= driver.find_element(By.XPATH, '//*[@id="__next"]/header/div[1]/section/div[2]/div[1]/div/form/input')
    search_box.send_keys('VNI30')
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    mouse = driver.find_element(By.XPATH, '//*[@id="fullColumn"]/div/div[2]/div[2]/div[1]/a')
    mouse.click()
    # Locate mouse to the News Category
    news_folder = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/nav/div[1]/ul/li[3]/a')
    news_folder.click()
    time.sleep(5)

    ########### Crawling

    # locate the > icon
    with tqdm(desc="Crawling pages") as pbar:
        while True:
            # Crawl all the link
            new_containers = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[2]/ul/li')
            for new in new_containers:
                new_data = {
                    "Website": "VnInvesting.com"
                }
                # Find Published Date
                pointer = new.find_element(By.XPATH, './article/div/ul/li[2]/time')
                day = pointer.get_attribute('datetime')
                # Find new link
                pointer = new.find_element(By.XPATH, './/a')
                path = pointer.get_attribute('href')

                # Save to data
                new_data['Date']= day
                new_data['Path']= path
                news_data.append(new_data)

            # Scroll to next page
            try:
                next_icon = driver.find_element(By.XPATH,\
                        f'//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/div[3]/a[2]')
                next_icon.click()
                time.sleep(5)
                pbar.update(1) 

            except Exception as e:
                print(f'Next icon is not available')
                break



    driver.quit()





    # Content Crawling

    for i in tqdm(range(len(news_data), desc="Scraping Articles")):
        response = requests.get(news_data[i]['Path'])
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the article container
        article_container = soup.find('div', id='article')

        # Extract paragraphs from the article
        if article_container: 
            paragraphs = article_container.find_all('p')
            article_text = '\n'.join([p.get_text() for p in paragraphs])
        else:
            article_text = "No content found"
        
        news_data[i]['Content'] = article_text


    print('Finished Crawling')
    return news_data


