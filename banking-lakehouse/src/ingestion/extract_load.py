import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

def authenticate_google_drive():
    try:
        cred_path = os.getenv("GOOGLE_CREDENTIALS_PATH") #key

        SCOPES = ['https://www.googleapis.com/auth/drive.readonly'] #permission

        creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES) #badge

        service = build('drive', 'v3', credentials=creds) #helper(we hire a person to helps us to talk googlish with our badge)
        
        print("Messgae from help: Hey I'm in!")
        return service
        
    except Exception as e:
        print(f"Error: help stuck with a problem - {e}")
    

if __name__ == "__main__":
    driver_service = authenticate_google_drive()