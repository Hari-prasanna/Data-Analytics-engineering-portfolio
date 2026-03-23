# 🛒 Shopstream: End-to-End Clickstream Analytics Pipeline

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=Databricks&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## 📌 Project Overview
Shopstream is an automated, enterprise-grade data pipeline built to process raw e-commerce clickstream events into business-ready conversion funnel analytics. 

The pipeline ingests raw Kaggle dataset events, converts them to columnar Parquet format for optimized storage, and lands them in **AWS S3**. From there, **Databricks** and **dbt** take over, processing the data through a Medallion Architecture (Bronze, Silver, Gold) to power downstream BI dashboards.

## 📊 The Business Value
This pipeline was built to answer critical e-commerce business questions:
* **The Conversion Funnel:** At what exact stage (View -> Cart -> Checkout -> Purchase) are users abandoning the platform?
* **Product Performance:** Which specific product categories generate the highest volume of views but the lowest conversion rates?
* **Session Analytics:** How does session duration correlate with successful purchases?

## 🏗️ Architecture & Data Flow
1. **Ingestion (Python -> S3):** A custom Python script extracts the raw dataset from Kaggle, converts it to Parquet for compression and performance, and securely loads it into an AWS S3 bucket.
2. **Raw Layer (Raw):** Databricks Auto Loader / external tables read the raw Parquet files directly from S3.
3. **Bronze Layer (Cleaned & Conformed):** Data is deduplicated, timestamps are standardized, and surrogate keys are generated.
4. **Gold Layer (Business Aggregates):** Dimensional models (`dim_users`, `dim_products`) and Fact tables (`fct_session_funnel`) are built for direct querying.

## 🚀 Key Engineering Highlights

This project goes beyond basic SQL transformations and implements production-level Data Engineering best practices:

* **Cloud Security & IAM:** Configured robust AWS IAM Roles and strict least-privilege permission policies to allow Databricks secure access to S3 without hardcoding credentials.
* **Service Principals for Automation:** Replaced vulnerable Personal Access Tokens (PATs) with Databricks Service Principals, ensuring secure, machine-to-machine authentication for CI/CD deployments.
* **Smart Incremental Processing:** Implemented dbt incremental models to only process newly landed S3 files. Utilized the `md5()` function on `user_session` , `user_id`, `Product_id`, `event_type`, `event_time` to generate deterministic **Surrogate Keys**, ensuring accurate deduplication and efficient upserts without scanning historical data.
* **Delta Lake Optimization:** Applied `ZORDER` clustering and `VACUUM` policies to optimize file sizes and skip irrelevant data during BI queries.
* **Data Governance:** Utilized **Databricks Unity Catalog** to implement Dynamic Data Masking (DDM), ensuring Personally Identifiable Information (PII) is hidden from unauthorized users.

## 🛠️ Tech Stack
* **Cloud Infrastructure:** AWS (S3, IAM)
* **Compute & Storage:** Databricks, Delta Lake
* **Transformation & Modeling:** dbt (Data Build Tool), PySpark, SQL
* **Governance & Security:** Unity Catalog, Service Principals
* **Orchestration / CI-CD:** GitHub Actions, Databricks Asset Bundles (DABs)

## 📂 Repository Structure
```text
clickstream-conversion-pipeline/
├── kaggle_s3_ingestion.py   # Python script converting raw data to Parquet & loading to S3
├── shopstream_dbt/          # dbt project containing Medallion models
│   ├── models/
│   │   ├── staging/         # Bronze to Silver transformations
│   │   └── gold/            # Silver to Gold business logic
│   └── dbt_project.yml      # dbt configuration
├── databricks_infra/        # Infrastructure & Governance notebooks
│   ├── setup_catalog.sql    # Unity Catalog environment setup
│   ├── Ingesting.ipynb      # S3 connection and Bronze layer ingestion
│   └── PPI_DDM_practice.sql # Dynamic Data Masking implementation
└── README.md