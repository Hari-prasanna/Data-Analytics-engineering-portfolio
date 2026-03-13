"""
TMDB Cloud Data Pipeline (Extract & Load)
=========================================
Extracts movie data from the TMDB API and vacuum-seals it directly 
into an AWS S3 Data Lake as Parquet files.
"""

import os
import time
import json
from datetime import datetime, timezone
from io import BytesIO

import pandas as pd
import requests
import boto3

# Safely load local .env file (Ignored perfectly by GitHub Actions!)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# =============================================================================
# CONFIGURATION & SECRETS
# =============================================================================

TMDB_BASE_URL = "https://api.themoviedb.org/3"
RELEASE_DATE_START = "2026-01-01"
RELEASE_DATE_END = "2026-12-31"
DEFAULT_MAX_PAGES = 5
API_RATE_LIMIT_DELAY = 0.1
PROGRESS_LOG_INTERVAL = 20

# These are automatically populated by GitHub Secrets in the cloud!
API_KEY = os.getenv("TMDB_API_KEY")
AWS_BUCKET = os.getenv("AWS_S3_BUCKET")


# =============================================================================
# THE CHEF: Extract from TMDB API
# =============================================================================

def fetch_base_movies(max_pages=DEFAULT_MAX_PAGES):
    """Fetch base movie listings from TMDB discover endpoint."""
    print(f"\n👨‍🍳 Step 1: Fetching {max_pages} pages of base movies...")
    url = f"{TMDB_BASE_URL}/discover/movie"
    movies = []

    for page_num in range(1, max_pages + 1):
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "primary_release_date.gte": RELEASE_DATE_START,
            "primary_release_date.lte": RELEASE_DATE_END,
            "sort_by": "popularity.desc",
            "page": page_num,
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            movies.extend(response.json().get("results", []))
        time.sleep(API_RATE_LIMIT_DELAY)

    print(f"  ✅ Fetched {len(movies)} base movies")
    return movies

def fetch_details_and_credits(movie_ids):
    """Fetch details and credits for multiple movies."""
    print(f"\n🕵️ Step 2: Fetching details & credits for {len(movie_ids)} movies...")
    details_list = []
    credits_list = []

    for count, movie_id in enumerate(movie_ids, start=1):
        if count % PROGRESS_LOG_INTERVAL == 0:
            print(f"  Processing: {count}/{len(movie_ids)} movies...")

        # Get Details
        det_resp = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params={"api_key": API_KEY})
        if det_resp.status_code == 200:
            details_list.append(det_resp.json())

        # Get Credits
        cred_resp = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}/credits", params={"api_key": API_KEY})
        if cred_resp.status_code == 200:
            credits_list.append(cred_resp.json())

        time.sleep(API_RATE_LIMIT_DELAY)

    print(f"  ✅ Collected {len(details_list)} movie details")
    print(f"  ✅ Collected {len(credits_list)} movie credits")
    return details_list, credits_list


# =============================================================================
# THE DRIVER: Load Data to AWS S3
# =============================================================================

def serialize_complex_columns(df):
    """Parquet requires strict data types. This converts messy lists/dicts to text."""
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: json.dumps(x) if isinstance(x, (dict, list)) else x
        )
    return df

def upload_to_s3(data: list[dict], file_name: str):
    """Converts data to Parquet and uploads to S3."""
    if not data:
        print(f"  ⚠️ No data to load for '{file_name}'")
        return

    # 1. Prep the DataFrame
    df = pd.DataFrame(data)
    df = serialize_complex_columns(df)
    df["loaded_at"] = datetime.now(timezone.utc)
    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"])

    # 2. Connect to AWS 
    # (Notice I added a fallback 'eu-central-1' region so it can't crash on None!)
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'eu-central-1') 
    )

    # 3. Create the floating RAM container
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, engine='pyarrow', index=False)
    
    # 4. Deliver the package to the 'raw' folder
    s3_key = f"tmdb-elt/raw/{file_name}.parquet"
    print(f"  🚚 Uploading {len(df)} rows to s3://{AWS_BUCKET}/{s3_key}...")
    
    s3_client.put_object(
        Bucket=AWS_BUCKET,
        Key=s3_key,
        Body=parquet_buffer.getvalue()
    )


# =============================================================================
# THE MANAGER'S DESK: Run Pipeline
# =============================================================================

if __name__ == "__main__":
    print("🚀 Starting Cloud TMDB Pipeline...")
    
    # Check if critical secrets are missing before doing any work!
    if not API_KEY or not AWS_BUCKET:
        print("❌ ERROR: Missing API_KEY or AWS_BUCKET. Check your .env or GitHub Secrets!")
        exit(1)
        
    # 1. Extract
    base_movies = fetch_base_movies(max_pages=DEFAULT_MAX_PAGES)
    movie_ids = [movie["id"] for movie in base_movies]
    movie_details, movie_credits = fetch_details_and_credits(movie_ids)

    # 2. Load directly to S3
    print("\n📦 Step 3: Pushing data to AWS S3 Data Lake...")
    upload_to_s3(base_movies, "raw_movies")
    upload_to_s3(movie_details, "raw_movie_details")
    upload_to_s3(movie_credits, "raw_movie_credits")

    print("\n🎉 Pipeline complete! All raw files are safely in S3.")
