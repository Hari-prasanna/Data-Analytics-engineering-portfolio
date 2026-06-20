# Shopstream: End-to-End Clickstream Analytics Pipeline

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=Databricks&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Automated pipeline processing raw e-commerce clickstream events into conversion funnel analytics. Raw Kaggle events are converted to Parquet and landed in AWS S3. Databricks and dbt process them through a Medallion Architecture (Bronze → Silver → Gold) to answer conversion and session-quality questions for downstream BI.

- Ingestion script — [kaggle_s3_ingestion.py](kaggle_s3_ingestion.py)
- dbt project — [shopstream_dbt/](shopstream_dbt/)
- Unity Catalog setup — [databricks_infra/setup_catalog.sql.dbquery.ipynb](databricks_infra/setup_catalog.sql.dbquery.ipynb)
- Dynamic Data Masking — [databricks_infra/PPI - DDM practice.sql.dbquery.ipynb](<databricks_infra/PPI - DDM practice.sql.dbquery.ipynb>)

---

## Business Questions Answered

| Question | Model |
| :--- | :--- |
| At what funnel stage (View → Cart → Checkout → Purchase) are users abandoning? | `fct_session_funnel` |
| Which product categories have the highest view-to-purchase drop-off? | `dim_products` joined to `fct_session_funnel` |
| How does session duration correlate with purchase conversion? | `fct_session_funnel` |

---

## Architecture

```
Kaggle Dataset (raw CSV events)
    │
    ▼ kaggle_s3_ingestion.py  (Parquet conversion → S3 upload)
AWS S3 — raw Parquet files
    │
    ▼ Databricks Auto Loader / external tables
Bronze Delta table — raw events (deduplicated, timestamps standardized)
    │
    ▼ dbt-databricks (Silver)
stg_events — surrogate key on user_session + user_id + product_id + event_type + event_time
    │
    ▼ dbt-databricks (Gold)
    ├── dim_users           ← User dimension
    ├── dim_products        ← Product dimension
    └── fct_session_funnel  ← Conversion funnel fact per session
```

---

## Key Engineering Details

| Technique | Where it's used |
| :--- | :--- |
| **Surrogate key generation** | `md5()` on five session/event fields — deterministic deduplication without scanning historical data |
| **Incremental processing** | dbt incremental models only process newly landed S3 files — no full-table scans on reruns |
| **Dynamic Data Masking** | Unity Catalog DDM hides PII (user IDs) from unauthorized roles while leaving analytical columns visible |
| **ZORDER clustering** | Applied on high-cardinality query columns to reduce data scanned per BI query |
| **IAM + Service Principals** | Databricks accesses S3 via IAM role; CI/CD deploys via Service Principal — no PATs or hardcoded credentials |

---

## Setup

### Prerequisites

- AWS account with an S3 bucket and IAM role configured for Databricks access
- Databricks workspace with Unity Catalog enabled
- Kaggle API credentials

### 1) Configure environment

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `KAGGLE_USERNAME` | Kaggle account username |
| `KAGGLE_KEY` | Kaggle API key |
| `S3_BUCKET` | Target S3 bucket name |
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |

### 2) Ingest raw data

```bash
pip install -r requirements.txt
python kaggle_s3_ingestion.py
```

### 3) Configure Unity Catalog

Run [databricks_infra/setup_catalog.sql](databricks_infra/setup_catalog.sql) in a Databricks SQL session to create the catalog, schemas, and external location pointing to S3.

### 4) Run Bronze ingestion

Open and run [databricks_infra/Ingesting.ipynb](databricks_infra/Ingesting.ipynb) in Databricks to read the S3 Parquet files into the Bronze Delta table.

### 5) Run dbt transformations

```bash
cd shopstream_dbt
dbt deps
dbt run --target dev
dbt run --target prod
dbt test
```

---

## Project Layout

```
clickstream-conversion-pipeline/
├── kaggle_s3_ingestion.py        ← Kaggle → Parquet → S3
│
├── shopstream_dbt/               ← dbt project (Medallion: Bronze → Silver → Gold)
│   ├── models/
│   │   ├── staging/              ← Bronze → Silver: deduplicate, surrogate key
│   │   └── gold/                 ← Silver → Gold: dimensions and funnel fact
│   └── dbt_project.yml
│
└── databricks_infra/
    ├── setup_catalog.sql         ← Unity Catalog environment setup
    ├── Ingesting.ipynb           ← S3 → Bronze Delta table
    └── PPI_DDM_practice.sql      ← Dynamic Data Masking policy
```

---

## Notes

- **Parquet over CSV:** The ingestion script converts raw CSV to Parquet before uploading to S3. This cuts storage size by ~70% and makes Databricks reads significantly faster due to columnar compression.
- **DDM scope:** Dynamic Data Masking is applied at the Unity Catalog column policy level. Users with the `analyst` role see masked `user_id` values; users with `data_engineer` or above see the raw values. No application-level logic required.
- **CI/CD:** GitHub Actions deploys dbt model changes to the Databricks workspace via Databricks Asset Bundles (DABs) using a Service Principal — no human credentials are involved in the deployment path.
