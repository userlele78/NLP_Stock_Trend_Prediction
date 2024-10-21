# Dataframe
import pandas as pd

# Web Crawling
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Other
import time
from tqdm import tqdm
from utils import parse_date, StockNewsCrawler, crawl_news_for_keyword
import os

'''  CRAWLING PROCESS '''


def search_for_keyword_Vninvesting(driver, keyword):
    # Find the search box
    seach_key_locating = driver.find_element(By.XPATH, '//*[@id="__next"]/header/div[1]/section/div[2]/div[1]/button')
    seach_key_locating.click()

    search_box= driver.find_element(By.XPATH, '//*[@id="__next"]/header/div[1]/section/div[2]/div[1]/div/form/input')
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    mouse = driver.find_element(By.XPATH, '//*[@id="fullColumn"]/div/div[2]/div[2]/div[1]/a')
    mouse.click()
    # Locate mouse to the News Category
    news_folder = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[2]/div[1]/nav/div[1]/ul/li[3]/a')
    news_folder.click()
    time.sleep(5)
    


def crawl_vninvesting_news(driver, keyword):
    '''  Take all news links  '''
    news_data = []
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
                new_data['Date']= parse_date(day)
                new_data['Path']= path
                new_data['Segment'] = keyword

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
    '''  Take all news contents  '''
    for i in tqdm(range(len(news_data)), desc="Scraping Articles"):
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

    print(f'Finished Crawling VnInvesting.com with {keyword}')
    return news_data


# Note

'''
When searching keyword about index, this is a code for it

When it comes to others, we need to locate 'Tin tuc' category and as we scroll down the page, the news comes up 


'''


if __name__ == "__main__":
    link = 'https://vn.investing.com/'
    keyword = 'Ngân hàng'
    crawler = StockNewsCrawler()
    crawl_news_for_keyword(crawler, link, search_for_keyword_Vninvesting, crawl_vninvesting_news, keyword)
