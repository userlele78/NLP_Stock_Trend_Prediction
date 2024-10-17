''' 
    This py file represent the whole pipeline of the data 

'''
from crawl_data import *
from store_data import *
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


# Crawling

# Saving


# Read data -- with other user
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_ID = '1vsLkkxsR5dHemeh7wPyGYoKIvA2xIT-1'
SECRET_FILE = os.path.join(BASE_DIR, '..', '..', 'dunp1710_client_secrets.json')
FILE_ID = '1eSnLAt-pfIvpxtU_YABIxbjvaBLpktKU'

google_auth = GoogleAuth()
google_auth.LoadClientConfigFile(SECRET_FILE)
google_auth.LocalWebserverAuth()
drive_app = GoogleDrive(google_auth)

# Create a file object using the file_id
file = drive_app.CreateFile({'id': FILE_ID})

# Download the file to the local environment
local_filename = os.path.join(BASE_DIR, 'downloaded_file.csv')
file.GetContentFile(local_filename)
print(f'File downloaded to {local_filename}')


