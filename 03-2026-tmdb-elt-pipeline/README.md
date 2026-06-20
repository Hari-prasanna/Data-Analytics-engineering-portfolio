# TMDB Analytics Engine: Local to Cloud Lakehouse

End-to-end ELT pipeline extracting movie and financial data from the TMDB API. The project has two generations: a local Postgres proof-of-concept (V1) and a fully cloud-hosted architecture on AWS S3 and Databricks (V2). Both generations are protected by a GitHub Actions CI/CD pipeline.

> **Live dbt documentation:** [View data lineage and model docs](https://hari-prasanna.github.io/Data-Analytics-engineering-portfolio/#!/overview)

- V1 Python extraction — [load_movies.py](load_movies.py)
- V2 cloud extraction — [cloud_pipeline/extract_to_s3.py](cloud_pipeline/extract_to_s3.py)
- V1 dbt project — [Movie_data_transformation/](Movie_data_transformation/)
- V2 dbt project — [cloud_pipeline/databricks_cloud/](cloud_pipeline/databricks_cloud/)
- Airflow orchestration — [../03-2026-airflow-orchestration/](../03-2026-airflow-orchestration/)

---

## Architecture

### V2: Cloud Data Lakehouse (Current)

```
TMDB REST API
    │
    ▼ cloud_pipeline/extract_to_s3.py  (io.BytesIO — no local disk I/O)
AWS S3 — raw Parquet files
    │
    ▼ Databricks Auto Loader
Unity Catalog — Bronze Delta table
    │
    ▼ dbt-databricks (Serverless compute)
Silver / Gold Star Schema
    │
    ▼ Apache Airflow (Dockerized)
Orchestrated daily — Python extract → dbt build
```

### V1: Local Postgres (Legacy)

```
TMDB REST API
    │
    ▼ load_movies.py  (Pandas → SQLAlchemy)
Local PostgreSQL — raw schema
    │
    ▼ dbt-postgres
Staging → Marts Star Schema
    │
    ▼ GitHub Actions CI/CD
Ephemeral Postgres · Python extract · dbt build on every PR
```

---

## Tech Stack

| Category | Technologies |
| :--- | :--- |
| Data Storage | AWS S3 · PostgreSQL *(Legacy)* |
| Compute & Governance | Databricks · Unity Catalog · Delta Lake |
| Transformation | dbt (`dbt-databricks` · `dbt-postgres`) |
| Orchestration | Apache Airflow (Dockerized via Astronomer CLI) |
| CI/CD & Security | GitHub Actions · GitHub Environments |

---

## Key Engineering Details

| Technique | Where it's used |
| :--- | :--- |
| **In-memory streaming** | `io.BytesIO` buffers API pages directly to S3 — no local disk write, no OOM risk on large paginated responses |
| **Clean-room venv isolation** | Airflow `BashOperator` tasks each create a disposable `/tmp/` virtualenv, preventing dependency conflicts between Airflow and the pipeline |
| **Path-filtered CI/CD** | GitHub Actions uses `paths:` filtering to trigger only when relevant monorepo files change, avoiding unnecessary compute spend |
| **Secrets isolation** | GitHub Environments gate Postgres credentials, AWS keys, and Databricks tokens — no hardcoded values in any script |
| **dbt data quality** | `not_null`, `unique`, and `accepted_values` tests enforce data contract before data reaches the presentation layer |

---

## Local Setup (V1 Postgres)

*The V2 cloud architecture requires an active AWS account and Databricks workspace. To run the legacy local version:*

### 1) Configure environment

```bash
git clone <repository-url>
cd TMDB-ELT
cp .env.example .env
```

| Variable | Description |
|---|---|
| `TMDB_API_KEY` | API key from developer.themoviedb.org |
| `DB_USER` | Postgres username |
| `DB_PASSWORD` | Postgres password |
| `DB_NAME` | Database name |
| `DB_HOST` | Database host (default: `localhost`) |
| `DB_PORT` | Database port (default: `5432`) |

### 2) Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3) Run the pipeline

```bash
# Extract and load raw data into Postgres
python load_movies.py

# Build and test dbt models
cd Movie_data_transformation
dbt build
```

---

## Project Layout

```
TMDB-ELT/
├── load_movies.py                      ← V1 Python extraction (Pandas → Postgres)
├── requirements.txt
│
├── Movie_data_transformation/          ← V1 dbt project (dbt-postgres)
│   ├── models/
│   │   ├── staging/                    ← Raw → Silver transformations
│   │   └── marts/                      ← Silver → Gold dimensional models
│   └── dbt_project.yml
│
├── cloud_pipeline/
│   ├── extract_to_s3.py                ← V2 Python extraction (BytesIO → S3)
│   └── databricks_cloud/              ← V2 dbt project (dbt-databricks)
│       ├── models/
│       │   ├── staging/
│       │   └── marts/
│       └── dbt_project.yml
│
└── .env.example
```

---

## Notes

- **V1 CI/CD:** The GitHub Actions workflow spins up a temporary Postgres service container, runs `load_movies.py`, then runs `dbt build` — all against the ephemeral database. No persistent infrastructure is needed for PR validation.
- **V2 IAM:** Databricks accesses S3 via an IAM role and External Location — no AWS keys are stored inside the workspace. The role trust policy restricts access to the specific Databricks account and credential path.
- **Pagination:** The TMDB API paginates results. The extraction script handles `total_pages` and loops until all pages are collected, writing each page to the same S3 path in append mode.
