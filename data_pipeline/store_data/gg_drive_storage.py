
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

FOLDER_ID = '1vsLkkxsR5dHemeh7wPyGYoKIvA2xIT-1'
SECRET_FILE = os.path.abspath(os.path.join(os.getcwd(), 'dam0709123_client_secrets.json'))

# Authenticate Google Drive
def authenticate_google_drive():
    google_auth = GoogleAuth()
    google_auth.LoadClientConfigFile(SECRET_FILE)
    google_auth.LocalWebserverAuth()  
    drive_app = GoogleDrive(google_auth)
    return drive_app

# Upload to Google Drive
def upload_to_gg_drive(data): 
    drive_app = authenticate_google_drive()
    
    file = drive_app.CreateFile({
        'parents': [{'id': FOLDER_ID}],
        'title': 'Data'  
        })
    file.SetContentFile(data)
    file.Upload()
    file_id = file['id']
    print(f'Uploaded file to Google Drive with ID: {file_id}')
    
    return file_id

# Set folder public
def set_folder_public(folder_id):
    drive_app = authenticate_google_drive()
    
    permission = {
        'role': 'writer',
        'type': 'anyone', 
    }

    folder = drive_app.CreateFile({'id': folder_id})
    folder.InsertPermission(permission)

    print(f'Folder with ID {folder_id} is now public.')


if __name__ == '__main__':
    # data = [
    #     {'dict': '1'},
    #     {'dict1': '2'}
    # ]
    # data = pd.DataFrame(data)
    # # Use StringIO to create an in-memory CSV
    # file_path = os.path.join(BASE_DIR, '..', '..', '..' ,'data.csv')
    # file_id = upload_to_gg_drive(file_path)
    # set_folder_public(FOLDER_ID)
    # print(file_id)
    pass




