import os
import logging
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. Setup the "Announcement System" (Logging)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv() # Added () here!

def google_authentication():
    logging.info("Starting the connection...") # Lowercase info()
    try:
        cred_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        if not cred_path:
            logging.error("Credentials path not found in .env!")
            return None

        SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

        # This line builds your "Badge" (Explained below)
        creds = service_account.Credentials.from_service_account_file(
            cred_path, 
            scopes=SCOPES
        )

        service = build('drive', 'v3', credentials=creds)
        logging.info("Successfully connected to Google Drive!")
        return service
        
    except Exception as e:
        logging.error(f"Failed to connect: {e}")
        return None

# The "Safety Switch" (Explained below)
if __name__ == "__main__":
    drive_service = google_authentication()