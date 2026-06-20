import logging
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv
import boto3


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def google_authentication(cred_path):
    logging.info("Preparing badge for the walkie-talkie (service) to talk with google warehouse")
    
    try:
        key = cred_path #key
        if not key:
            logging.error("oppsie! key path is missing!")
            return None
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly'] #permission

        badge = service_account.Credentials.from_service_account_file(key, scopes=SCOPES) #badge to use walkie-talkie (service)

        service = build('drive', 'v3', credentials= badge) #ẃalkie-talkie acessing by badge (service acc) 
        logging.info("Py Driver: badge is accessed I can now talk to the warehouse clerk")
        return service
    except Exception as e:
        logging.error(f"Error in block 1: {e}")


def downloading_from_google_drive(service, folder_id, file_name, download_path):
    try:
        logging.info(f"Communicationg with Google warehouse clerk to check {folder_id} & {file_name}")
        query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"

        results = service.files().list(q=query).execute() #talking to the clerk with walkie-takie and pressing the button(execute) to start searching
        items = results.get("files",[]) #recived the files, now avoiding crashing by using get that gives empty if nothing is inside

        if not items:
            logging.error("warehouse clerk to py driver - we don't have the exact file name you mentioned")
            return None
        
        file_id = items[0]["id"] #looking for first file and taking id for requesting content
        logging.info(f"we have got the {items[0]['name']}'s id: {file_id}")

        request_content = service.files().get_media(fileId=file_id) #requesting content using file_id to transger to local file

        with open(download_path, 'wb') as local_file: #wb: write binary as the csv or other file doesn't support internal lang
            donwload = MediaIoBaseDownload(local_file, request_content) #downling as batch using Io

            done = False # if true immediatley stops the while loop 
            while done is False:
                status, done = donwload.next_chunk() # if done status is still false then it is chunked and status helps to track 
                logging.info(f"py driver loading: {int(status.progress() * 100)}%") #status gives the decimal values and converted to int(whole number) and mulitiplied to 100 and adding suffix will show how many % is downloaded in each chunk
        logging.info("truck is loaded and ready to head AWS warehouse")   
        return download_path
    

    except Exception as e:
        logging.error(f"Error in block 2: {e}")


def upload_to_s3(local_path, bucket_name, s3_key):
    try:
        s3_client = boto3.client('s3') #takes the secret key and ID automatically from .env

        s3_client.upload_file(
            Filename = local_path,
            Bucket = bucket_name,
            Key = s3_key
        )
        return True

    except Exception as e:
        logging.error(f"Error in block 3: {e}")


if __name__ == "__main__":

#config
    cred_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    download_path = os.getenv("DOWNLOAD_PATH")
    file_name = "SFD_Fraud Detection_1.csv"
    bucket_name = os.getenv("S3_LANDING_BUCKET")
    s3_key = f"banking-lakehouse/raw_data/{file_name}"

#execution
    service_delivery = google_authentication(cred_path)

    if service_delivery:
        download = downloading_from_google_drive(service_delivery,folder_id,file_name,download_path)
    else:
        logging.error("Error with google_auth_final block 1")
    if download:
        send_to_s3 = upload_to_s3(download, bucket_name, s3_key)
        logging.info(f"The {file_name} has been successfully unloaded in AWS warehouse inisde {bucket_name}")
        if os.path.exists(download):
            os.remove(download)
            logging.info("local files removed after uploading")
    else:
        logging.error("Error with downloading the file")