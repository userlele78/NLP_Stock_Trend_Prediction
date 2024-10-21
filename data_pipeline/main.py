''' 
    This py file represent the whole pipeline of the data 

'''
from crawl_data import *
from store_data import *
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from tqdm import tqdm



# Crawling
KEYWORDS = ['Ngân hàng', 'Tài chính']
WEBLINKS = ['https://vietstock.vn/', 'https://vn.investing.com/']
stock_news = StockNewsCrawler()



for keyword in tqdm(KEYWORDS, desc="Crawling stock news"):
    crawl_news_for_keyword(stock_news, WEBLINKS[1], search_for_keyword_Vninvesting, crawl_vninvesting_news, keyword)
    crawl_news_for_keyword(stock_news, WEBLINKS[0], search_for_keyword_Vietstock, crawl_vietstock_news, keyword)


# Saving

data = pd.DataFrame(stock_news.news_data)
file_path = os.path.join(BASE_DIR, '..', '..' ,'data.csv')
data.to_csv(file_path, index=False, encoding='utf-8')
file_id = upload_to_gg_drive()
set_folder_public(FOLDER_ID)
print(file_id)




# Read data -- with other user
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FOLDER_ID = '1vsLkkxsR5dHemeh7wPyGYoKIvA2xIT-1'
# SECRET_FILE = os.path.join(BASE_DIR, '..', '..', 'dunp1710_client_secrets.json')
# FILE_ID = '1eSnLAt-pfIvpxtU_YABIxbjvaBLpktKU'

# google_auth = GoogleAuth()
# google_auth.LoadClientConfigFile(SECRET_FILE)
# google_auth.LocalWebserverAuth()
# drive_app = GoogleDrive(google_auth)

# # Create a file object using the file_id
# file = drive_app.CreateFile({'id': FILE_ID})

# # Download the file to the local environment
# local_filename = os.path.join(BASE_DIR, 'downloaded_file.csv')
# file.GetContentFile(local_filename)
# print(f'File downloaded to {local_filename}')


