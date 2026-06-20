import pandas as pd
import logging
import json
from google.oauth2.service_account import Credentials
import gspread

logging.basicConfig(level=logging.INFO, format= '%(asctime)s - %(levelname)s - %(message)s)')

def get_credentials(sheet_name, sheet_id):
    try:
        logging.info("taking credentials from cloud")

        secrets = dbutils.secrets.get(scope="my-secrets", key="google-auth") #getting secerets securly

        scopes = ['https://www.googleapis.com/auth/spreadsheets'] #permissions

        wraping_to_json = json.loads(secrets) #coverting text to string

        cred = Credentials.from_service_account_info(wraping_to_json, scopes=scopes) # creating badge

        client = gspread.authorize(cred) #creating our client to work with google sheets

        return client.open_by_key(sheet_id).worksheet(sheet_name)
    
    except Exception as e:
        logging.error(f"Auth Error: {e}")
        return None

def getting_into_sheet(sheet):
    try:
        logging.info("getting inside the google sheet..")
        data = sheet.get_all_records() #getting all data from the sheet

        if not data:
            logging.warning("No data found in the sheet")
            return set() #if not data then empty set
    
        df = pd.DataFrame(data)
        
        return set(df['transaction_id'].astype(str)) #returning set of transaction_id (set: sorted column for python to read and compare)
    except Exception as e:
        logging.error(f"Error: {e}")
        return None
    

def getting_data_from_db():
    try:
        logging.info("getting data from db")

        query = "SELECT transaction_id, transaction_timestamp, transaction_amount FROM banking_lakehouse.gold.mart_fraud_dashboard WHERE is_fraud = TRUE"

        df_db = spark.sql(query).toPandas()

        return df_db
    except Exception as e:
        logging.error(f"Error: {e}")
        return None
    
def upload_to_sheet(sheet, db_df):
    try:
        logging.info("uploading data to sheet")

        google_sheet_record = getting_into_sheet(sheet) #getting the ids to compare
        
        db_df['transaction_id'] = db_df['transaction_id'].astype(str) #converting to string to compare

        for col in db_df.columns:
            if pd.api.types.is_datetime64_any_dtype(db_df[col]):
                logging.info(f"Converting column {col} from Timestamp to String...")
                db_df[col] = db_df[col].astype(str)

        filtered_records = db_df[~db_df['transaction_id'].isin(google_sheet_record)] #filtering the records which are not in google sheet

        if not sheet.get_all_values():
            headers = db_df.columns.tolist()
            sheet.insert_row(headers, 1) #if sheet is empty then add headers

        if not filtered_records.empty: #if there are new records then add the new records
            rows_to_add = filtered_records.fillna("").values.tolist() #converting to list
            sheet.append_rows(rows_to_add)
            logging.info(f"added {len(rows_to_add)} new rows to the sheet")
        else:
            logging.warning("No new records to add")
        
        return True
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    sheet_name = "test"
    sheet_id = "1lQpV0z-i9yUKsdG_LGst0PzJYo6tcUBXKo-JZED3kaM"

    sheet = get_credentials(sheet_name, sheet_id)
    
    if sheet:
        fraud_data = getting_data_from_db()
    
        if fraud_data is not None:
            upload_to_sheet(sheet, fraud_data)
    else:
        logging.error("Error with getting data from db")