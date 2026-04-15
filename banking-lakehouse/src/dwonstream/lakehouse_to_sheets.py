import json
import pandas as pd
import gspread 
from google.oauth2.service_account import Credentials
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_google_sheet(sheet_id, sheet_name):
    """Robot 1: Authenticates and returns the worksheet object."""
    try:
        logging.info("Accessing the Databricks Vault...")
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        secrets = dbutils.secrets.get(scope="my-secrets", key="google-auth")
        
        service_account_info = json.loads(secrets)
        cred = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(cred)

        return client.open_by_key(sheet_id).worksheet(sheet_name)
    except Exception as e:
        logging.error(f"Auth Error: {e}")
        return None
    
def get_existing_ids(sheet):
    """Robot 2: Gets ONLY the IDs from the sheet to help the bouncer."""
    try:
        records = sheet.get_all_records()
        if not records:
            return set()
        
        df = pd.DataFrame(records)
        return set(df['transaction_id'].astype(str))
    except Exception as e:
        logging.error(f"Error reading IDs: {e}")
        return set()

def get_records_from_db():
    """Robot 3: Fetches fraud data from the Lakehouse."""
    try:
        query = "SELECT transaction_id, transaction_timestamp, transaction_amount FROM banking_lakehouse.gold.mart_fraud_dashboard WHERE is_fraud = TRUE"

        return spark.sql(query).toPandas()
    except Exception as e:
        logging.error(f"DB Error: {e}")
        return None

def sync_records(sheet, db_df):
    """The Manager: Compares and pushes data."""
    
    existing_ids = get_existing_ids(sheet)
    
    db_df['transaction_id'] = db_df['transaction_id'].astype(str)
    
    for col in db_df.columns:
        if pd.api.types.is_datetime64_any_dtype(db_df[col]):
            logging.info(f"Converting column {col} from Timestamp to String...")
            db_df[col] = db_df[col].astype(str)
    

    new_records = db_df[~db_df['transaction_id'].isin(existing_ids)]


    if not sheet.get_all_values():
        headers = db_df.columns.tolist()
        sheet.insert_row(headers, 1)

    if not new_records.empty:
        rows_to_add = new_records.fillna("").values.tolist()
        sheet.append_rows(rows_to_add)
        logging.info(f"✅ Added {len(rows_to_add)} new rows.")

if __name__ == "__main__":
    S_ID = "1lQpV0z-i9yUKsdG_LGst0PzJYo6tcUBXKo-JZED3kaM"
    S_NAME = "test"
    
    my_sheet = get_google_sheet(S_ID, S_NAME)
    
    if my_sheet:
        fraud_data = get_records_from_db()
        
        if fraud_data is not None:
            sync_records(my_sheet, fraud_data)
            logging.info("Pipeline completed successfully.")