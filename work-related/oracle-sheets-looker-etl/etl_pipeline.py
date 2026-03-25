import oracledb
import gspread
import json
import pandas as pd
import pytz 
import time
import logging
import os
from datetime import datetime
from sqlalchemy import create_engine, text

# ==========================================
# 0. SETUP LOGGING & RUNTIME WIDGETS
# ==========================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("py4j").setLevel(logging.WARNING)

# ONLY ask the user for things that change per run
dbutils.widgets.text("category", "Beauty", "1. Product Category")
CATEGORY = dbutils.widgets.get("category")

# ==========================================
# 1. LOAD CONFIGURATION
# ==========================================
def load_config():
    # os.getcwd() gets the current folder the script is running inside
    current_folder = os.getcwd() 
    config_path = os.path.join(current_folder, "config.json")
    
    logger.info(f"⚙️ Loading configuration from current folder")
    with open(config_path, 'r') as f:
        return json.load(f)

# ==========================================
# 2. HELPER FUNCTIONS 
# ==========================================
def get_auth_clients():
    logger.info("🔑 Fetching credentials from Databricks Secrets...")
    
    # A. Google Auth
    google_secret = dbutils.secrets.get(scope="luu_qm_secrets", key="google_auth")
    gc = gspread.service_account_from_dict(json.loads(google_secret))

    # B. Oracle Auth
    oracle_config = json.loads(dbutils.secrets.get(scope="luu_qm_secrets", key="oracle_auth"))
    connection_string = (
        f"oracle+oracledb://{oracle_config['user']}:{oracle_config['password']}"
        f"@{oracle_config['host']}:{oracle_config['port']}/?service_name={oracle_config['service']}"
    )
    return create_engine(connection_string), gc

def extract_from_oracle(engine, sql_path, category):
    logger.info(f"📂 Reading SQL query & querying Oracle for: {category}...")
    with open(sql_path, 'r') as file:
        query = file.read()
        
    with engine.connect() as connection:
        df = pd.read_sql(text(query), connection, params={"category": category})
    
    logger.info(f"✅ Raw Data Extracted: {len(df)} rows.")
    return df

# ==========================================
# 3. MAIN EXECUTION
# ==========================================
def main():
    logger.info("🚀 STARTING JOB: Oracle -> Sheets -> Calc")
    berlin_tz = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(berlin_tz).strftime("%d/%m/%Y %H:%M:%S")
    
    try:
        # Load all our settings from the JSON file
        cfg = load_config()
        
        # --- INITIALIZATION & EXTRACT ---
        engine, gc = get_auth_clients()
        df_raw = extract_from_oracle(engine, cfg["file_paths"]["sql_query"], CATEGORY)
        
        if len(df_raw) == 0:
            raise ValueError("Oracle returned 0 rows. Aborting job.")

        # --- TRANSFORM ---
        logger.info("⚙️ Transforming data...")
        lhm_col = next((col for col in df_raw.columns if col.lower() == "mainlhm"), None)
        df_clean = df_raw[df_raw[lhm_col].astype(str).str.match(r'^\d')] if lhm_col else df_raw
        df_clean = df_clean.iloc[:, :22].fillna('')

        # --- LOAD ---
        logger.info("📋 Uploading to Sheets...")
        sh = gc.open_by_key(cfg["google_sheet"]["sheet_id"])
        
        worksheet_upload = sh.worksheet(cfg["google_sheet"]["upload_tab"])
        worksheet_upload.batch_clear(["A:V"])
        worksheet_upload.update(
            range_name="A1", 
            values=[df_clean.columns.values.tolist()] + df_clean.values.tolist()
        )
        
        try:
            sh.worksheet(cfg["google_sheet"]["time_tab"]).update_acell("C2", current_time)
        except Exception as e:
            logger.warning(f"Could not update time tab: {e}")

        logger.info("⏳ Waiting 5 seconds for Google Sheets formulas to sync...")
        time.sleep(5) 

        # --- CALCULATE ---
        logger.info(f"📥 Reading '{cfg['google_sheet']['calc_tab']}' for calculations...")
        worksheet_calc = sh.worksheet(cfg["google_sheet"]["calc_tab"])
        raw_data = worksheet_calc.get_all_values()
        
        if len(raw_data) <= 1:
            raise ValueError("Calculation Sheet was empty after sync!")

        # Calculate Total Vol (Index 11 / Col L)
        df_calc = pd.DataFrame(raw_data[1:], columns=raw_data[0])
        total_vol = pd.to_numeric(
            df_calc.iloc[:, 11].astype(str).str.replace(',', '').str.strip(), errors='coerce'
        ).fillna(0).sum()

        logger.info(f"✅ Total Volume: {total_vol}")

        # --- SUCCESS HANDOFF ---
        logger.info("💾 Saving Task Values for downstream jobs...")
        dbutils.jobs.taskValues.set(key="status", value="SUCCESS")
        dbutils.jobs.taskValues.set(key="rows", value=len(df_clean))
        dbutils.jobs.taskValues.set(key="total_vol", value=float(total_vol))
        dbutils.jobs.taskValues.set(key="ready_vol", value=float(total_vol))
        dbutils.jobs.taskValues.set(key="run_time", value=current_time)
        dbutils.jobs.taskValues.set(key="error_msg", value="")

    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR CAUGHT: {str(e)}")
        dbutils.jobs.taskValues.set(key="status", value="FAILURE")
        dbutils.jobs.taskValues.set(key="error_msg", value=str(e))
        dbutils.jobs.taskValues.set(key="rows", value=0)
        dbutils.jobs.taskValues.set(key="total_vol", value=0.0)
        dbutils.jobs.taskValues.set(key="ready_vol", value=0.0)
        dbutils.jobs.taskValues.set(key="run_time", value=current_time)
        raise e 

if __name__ == "__main__":
    main()