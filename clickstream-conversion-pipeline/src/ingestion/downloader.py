"""
ingest_and_convert.py
---------------------
Responsibility: Orchestrate the downloading of raw Kaggle data 
and its conversion into analytical Parquet chunks safely.
"""

import kaggle
import pandas as pd
import logging
from pathlib import Path

# --- Configuration & Logging Setup ---
RAW_FOLDER = Path("raw_data")
PARQUET_FOLDER = Path("raw_data/parquet")

# Configure a standard logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def setup_folders():
    """Creates necessary storage directories."""
    RAW_FOLDER.mkdir(exist_ok=True)
    PARQUET_FOLDER.mkdir(exist_ok=True)
    logger.info("Storage directories validated.")

def extract_from_kaggle():
    """Downloads and unzips the dataset. Represents the 'E' in ELT."""
    logger.info("Initiating dataset extraction from Kaggle API...")
    try:
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            "mkechinov/ecommerce-behavior-data-from-multi-category-store",
            path=str(RAW_FOLDER),
            unzip=True 
        )
        logger.info("Download and unzip complete.")
    except Exception as e:
        logger.error("Network or API failure during Kaggle extraction.")
        raise RuntimeError(f"Kaggle download failed — check network/kaggle.json: {e}") from e

def transform_to_parquet():
    """Finds the CSV and converts it to Parquet. Represents the 'T' in ELT."""
    csv_files = list(RAW_FOLDER.glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError("No CSV file found. Download phase likely failed.")
        
    csv_path = csv_files[0]
    logger.info(f"Target CSV located: {csv_path.name}. Beginning chunked conversion...")

    chunk_number = 0
    for chunk in pd.read_csv(csv_path, chunksize=100_000):
        chunk_number += 1
        output_filename = PARQUET_FOLDER / f"events_chunk_{chunk_number:04d}.parquet"
        chunk.to_parquet(output_filename, index=False)
        logger.info(f"Saved chunk {chunk_number:04d}: {len(chunk):,} rows")

    logger.info(f"Transformation complete. {chunk_number} Parquet files written.")

def main():
    """The main orchestrator function."""
    logger.info("=" * 50)
    logger.info("PIPELINE START: ShopStream — Phase 2 Ingestion & Conversion")
    logger.info("=" * 50)
    
    setup_folders()
    extract_from_kaggle()
    transform_to_parquet()

if __name__ == "__main__":
    main()