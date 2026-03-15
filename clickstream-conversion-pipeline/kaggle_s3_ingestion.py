"""
ingest_to_s3.py
---------------
ShopStream Phase 2 — Ingestion Pipeline
Responsibility: Download the Kaggle dataset, specifically extract ONLY 
the 2019-Oct.csv file to save disk space, stream it to S3, and clean up.
"""

import os
import io
import zipfile
import logging
import kaggle
import pandas as pd
import boto3
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

AWS_BUCKET      = os.getenv("AWS_S3_BUCKET")
AWS_REGION      = os.getenv("AWS_REGION", "eu-north-1")
S3_PREFIX       = "shopstream/raw/parquet"
KAGGLE_DATASET  = "mkechinov/ecommerce-behavior-data-from-multi-category-store"
TARGET_FILE     = "2019-Oct.csv"
CHUNK_SIZE      = 100_000 

LOCAL_TMP_DIR   = "raw_data"

# =============================================================================
# PIPELINE LOGIC
# =============================================================================
def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_REGION,
    )

def main():
    logger.info("Starting Phase 2 Ingestion: Targeted Extraction")
    
    if not os.path.exists(LOCAL_TMP_DIR):
        os.makedirs(LOCAL_TMP_DIR)

    # 1. Download the compressed ZIP to disk (do NOT unzip automatically)
    logger.info("Downloading dataset zip from Kaggle...")
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(KAGGLE_DATASET, path=LOCAL_TMP_DIR, unzip=False)
    
    # The zip file gets named after the last part of the dataset URL
    zip_filename = KAGGLE_DATASET.split('/')[-1] + ".zip"
    zip_file_path = os.path.join(LOCAL_TMP_DIR, zip_filename)

    # 2. Extract ONLY the October CSV
    logger.info(f"Extracting exactly what we need: {TARGET_FILE}...")
    with zipfile.ZipFile(zip_file_path, 'r') as zf:
        zf.extract(TARGET_FILE, path=LOCAL_TMP_DIR)

    # 3. Delete the massive zip file immediately to free up disk space
    logger.info("Extraction complete. Trashing the original zip file to save space.")
    os.remove(zip_file_path)

    # 4. Stream from Disk to S3
    csv_file_path = os.path.join(LOCAL_TMP_DIR, TARGET_FILE)
    s3 = get_s3_client()
    base_name = TARGET_FILE.replace(".csv", "")
    total_rows = 0
    chunk_num = 1

    logger.info("Streaming CSV in chunks to S3...")
    for chunk_df in pd.read_csv(csv_file_path, chunksize=CHUNK_SIZE):
        
        # Convert chunk to parquet in RAM
        parquet_buffer = io.BytesIO()
        chunk_df.to_parquet(parquet_buffer, engine="pyarrow", index=False)
        parquet_buffer.seek(0)
        
        s3_key = f"{S3_PREFIX}/{base_name}/chunk_{chunk_num:04d}.parquet"
        s3.put_object(Bucket=AWS_BUCKET, Key=s3_key, Body=parquet_buffer.getvalue())
        
        total_rows += len(chunk_df)
        logger.info(f"Uploaded chunk {chunk_num:04d} | Total Rows Processed: {total_rows:,}")
        chunk_num += 1

    # 5. Clean up the extracted CSV
    logger.info("Upload complete. Deleting the local CSV file...")
    os.remove(csv_file_path)
    
    logger.info(f"SUCCESS: Pipeline finished. {total_rows:,} rows landed in S3.")

if __name__ == "__main__":
    main()