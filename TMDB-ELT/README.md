# 🎬 TMDB Analytics Engine: Local to Cloud Data Lakehouse

**An end-to-end ELT (Extract, Load, Transform) pipeline that extracts movie and financial data from the TMDB API.** Originally built on a local PostgreSQL warehouse, this project was successfully migrated to an enterprise-grade Cloud Data Lakehouse architecture to improve scalability, security, and orchestration. The entire workflow is protected by a custom GitHub Actions CI/CD pipeline.

> 🔍 **Live Interactive Documentation:** [View the dbt Data Lineage & Docs Here](https://hari-prasanna.github.io/Data-Analytics-engineering-portfolio/#!/overview)

---

## 🛠️ Tech Stack Overview

| Category | Technologies Used |
| :--- | :--- |
| **Data Storage** | AWS S3, PostgreSQL *(Legacy)* |
| **Compute & Governance** | Databricks, Unity Catalog, Delta Lake |
| **Data Transformation** | dbt (`dbt-databricks`, `dbt-postgres`) |
| **Orchestration** | Apache Airflow *(Dockerized)* |
| **CI/CD & Security** | GitHub Actions, GitHub Environments |

---

## 🏗️ Architecture Evolution

### V2: Cloud Data Lakehouse *(Current)*
This modern architecture decouples storage from compute, utilizing the cloud for highly scalable data processing.

1. **Extract (Python & S3):** Connects to the TMDB REST API, handles pagination, and uses `io.BytesIO` buffers to stream data directly into AWS S3 as Parquet files, bypassing local disk I/O entirely.
2. **Load (Databricks):** Databricks reads the S3 external location and lands the data into a Unity Catalog Bronze layer as a highly efficient Delta Table.
3. **Transform (dbt-databricks):** Cleans and models the raw data into a dimensional Star Schema (Silver/Gold layers) using Databricks Serverless compute.
4. **Orchestrate (Apache Airflow):** A containerized Airflow environment manages the DAG execution, ensuring Python extraction and dbt transformations run in perfect sequence.

### V1: Local Modern Data Stack *(Legacy)*
The original proof-of-concept demonstrating a robust, localized data pipeline.

1. **Extract & Load (Python):** Python scripts processed the JSON responses via Pandas and loaded the raw data directly into a local PostgreSQL database.
2. **Transform (dbt-postgres):** Modeled the Postgres tables into a dimensional Star Schema optimized for downstream BI tools.
3. **CI/CD (GitHub Actions):** An automated "Traffic Cop" that spins up a temporary Postgres database, runs the Python extraction, and executes `dbt build` to rigorously test code integrity on every Pull Request.

---

## 🧠 Key Technical Achievements & Learnings

Building and migrating this project bridged the gap between writing standalone scripts and architecting enterprise-grade cloud pipelines.

| Achievement / Concept | Description & Impact |
| :--- | :--- |
| **Cloud Migration & Decoupled Architecture** | Successfully separated storage (AWS S3) from compute (Databricks). Configured AWS IAM roles and Databricks External Locations to securely pass data between cloud providers. |
| **In-Memory Data Streaming** | Engineered an Out-Of-Memory (OOM) proof ingestion script using Python's `io.BytesIO` and `boto3` to stream API data directly to S3 without writing to the local hard drive. |
| **Workflow Orchestration** | Implemented Apache Airflow to centralize pipeline execution, utilizing a "Clean Room" strategy via `BashOperators` to isolate Python virtual environments and prevent dependency conflicts. |
| **CI/CD Optimization** | Designed a GitHub Actions workflow using paths filtering to only trigger when specific monorepo files change, drastically saving cloud compute time. |
| **Security Best Practices** | Eliminated hardcoded credentials by implementing strict GitHub Environments to isolate database credentials, AWS keys, and Databricks tokens. |
| **Data Modeling** | Built reliable, tested data models using dbt, enforcing strict data quality rules before the data reaches the presentation layer. |

---

## 🚀 How to Run Locally (V1 Postgres Version)

*Note: The V2 Cloud architecture requires AWS and Databricks workspace access. To run the legacy local version, follow the steps below.*

**1. Clone the repository and navigate to the project folder:**
```bash
git clone <repository-url>
cd TMDB-ELT
```

**2. Create a `.env` file in the root directory with your credentials:**
```env
TMDB_API_KEY=your_api_key
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=postgres
DB_HOST=localhost
DB_PORT=5432
```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
# Alternatively, manually install: pandas, sqlalchemy, dbt-postgres, etc.
```

**4. Execute the pipeline:**
```bash
# Run the Python extraction
python load_movies.py

# Run the dbt models
cd Movie_data_transformation
dbt build
```
