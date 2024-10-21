# Dataframe
import pandas as pd

# Web Crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Other
from datetime import datetime, timedelta
import pytz
import time



def parse_date(day):
    current_time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    if 'giờ' in day:
        hours_ago = int(day.split(' ')[0]) 
        return current_time - timedelta(hours=hours_ago)
    else:
        return day 


def crawl_news_for_keyword(stock_class, weblink, source_func, crawl_func, keyword):
    driver = stock_class.setup_driver()
    driver.get(weblink)
    time.sleep(5)
    source_func(driver, keyword)
    news_data = crawl_func(driver, keyword)
    stock_class.append(news_data)


class StockNewsCrawler:
    def __init__(self):
        self.news_data = []

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
        driver = webdriver.Chrome(options=options)

        return driver