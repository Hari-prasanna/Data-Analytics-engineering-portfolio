import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging
import io # Helps us stream data chunk-by-chunk
from googleapiclient.http import MediaIoBaseDownload # The Google Loading Dock tool

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def google_authentication():
    logging.info("connecting to drive")
    try:
        cred_path = os.getenv("GOOGLE_CREDENTIALS_PATH") #key to lib door
        if not cred_path:
            logging.error("cred_path is not found in .env")
            return None

        SCOPES = ['https://www.googleapis.com/auth/drive.readonly'] #permission to only see the book 

        creds = service_account.Credentials.from_service_account_file(cred_path, scopes = SCOPES) #laminated badge with key + permission

        service = build('drive', 'v3', credentials=creds) #hiring a person(walkie talkie) who can talk googlish, and go inside the lib with our badge
        logging.info("Hepler: Hey I'm in with your badge!")

        return service
    except Exception as e:
        logging.error(f"Info from help: Ican't go in beacuse: {e}")
        return None

def download_files(service, folder_id, file_name, download_path):
    try:
        logging.info("starting the downloading process")

        query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false" #checking the folder and the filename, except trashed

        results = service.files().list(q=query).execute() #communicating with warehouse clerk and pressing executr button to send signal (to start)

        items = results.get("files",[]) #without crashing safely retun empty if the folder is empty by using get

        file_id = items[0]["id"] #getting the unique id for the first file in the folder
        logging.info(f"we have got the {items[0]['name']}'s id: {file_id}")

        if not file_id:
            logging.error("we don't have any files inside the folder")
            return None

        request_content = service.files().get_media(fileId=file_id) #requesting content for a specific file_id

        with open(download_path, 'wb') as local_file: #setting up the local file for write binary - internet lang
            download = MediaIoBaseDownload(local_file, request_content) #downloading ising the chunk (io) to thee local file from requested content

            done = False # if true immediatley stops the while loop 
            while done is False:
                status, done = download.next_chunk() # if done status is still false then it is chunked and status helps to track 
                logging.info(f"Dowloading {int(status.progress()*100)}%") #status gives the decimal values and converted to int(whole number) and mulitiplied to 100 and adding suffix will show how many % is downloaded in each chunk
        return download_path
            
    except Exception as e:
        logging.error(f"error: {e}")
        return None

if __name__ == "__main__":
    service_driver = google_authentication()
    downloading_files = download_files(service_driver,os.getenv("GOOGLE_DRIVE_FOLDER_ID"),"SFD_Fraud Detection_1.csv",os.getenv("DOWNLOAD_PATH"))

