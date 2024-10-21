# Dataframe
import pandas as pd

# Web Crawling
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
# Other
import time
from tqdm import tqdm
from .utils import *




'''        Viet Stock       '''

def search_for_keyword_Vietstock(driver, keyword):
    # Find the Seach key
    search_key = driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]/a[2]')
    search_key.click()
    time.sleep(5)
    # Input the seach box
    search_box= driver.find_element(By.XPATH, '//*[@id="popup-search-txt"]')
    search_box.send_keys(keyword)
    # Locate to news category
    news_folder = driver.find_element(By.XPATH, '//*[@id="search-tabs-wrapper"]/ul/li[6]/span')
    news_folder.click()
    time.sleep(5)

def crawl_vietstock_news(driver, keyword):
    news_data = []
    '''  Take all news links  '''
    clicked_time = 0
    with tqdm(desc="Clicking 'Xem them'") as pbar:
        while True:
            try:
                # locate the 'Xem them' icon and Click it
                next_icon = driver.find_element(By.XPATH, f'//*[@id="btn-see-more-list-news"]')
                next_icon.click()
                time.sleep(1)
                clicked_time += 1
                pbar.update(1)  # Progress bar will increase dynamically each time

            except Exception as e:
                print(f'Next icon is not available on time {clicked_time}: {e}')
                break

    news_container = driver.find_elements(By.XPATH, '//*[@id="list-news-search"]/li')
    for new in tqdm(news_container, desc="Crawling news links"):
        new_data = {
            "Website": "Vietstock.com"
        }
        # Find Published Date
        pointer = new.find_element(By.CLASS_NAME, 'news-publish-time')
        day = pointer.text.strip('()')

        # Find href element
        pointer = new.find_element(By.XPATH, './/a')
        path = pointer.get_attribute('href')

        # Save to data
        new_data['Date'] = parse_date(day)
        new_data['Path'] = path
        new_data['Segment'] = keyword

        news_data.append(new_data)
    driver.quit()


    '''  Take all news contents  '''
    # Take all the content from each news
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    for i in tqdm(range(len(news_data)), desc="Scraping Articles"):
        response = requests.get(news_data[i]['Path'], headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        article_container= soup.find('div',  class_="col-lg-8 col-sm-12 col-md-12 article-content")
        article_container = article_container.find('div', class_ = 'single_post_heading width_medium')
        if article_container: 
            paragraphs = article_container.find_all('p')
            article_text = '\n'.join([p.get_text() for p in paragraphs])
        else:
            article_text = "No content found"

        news_data[i]['Content'] = article_text

    print(f'Finished Crawling Vietstock.com with {keyword}')
    
    return news_data