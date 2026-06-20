# Banking Fraud Detection Lakehouse

Databricks lakehouse for financial fraud analysis built on a synthetic payment dataset. The pipeline tracks account risk profile changes over time using SCD Type 2 snapshots, enriches transactions with ML-style fraud-detection features, and pushes confirmed fraud records into an analyst-facing Google Sheet for daily triage.

- Ingestion script — [src/ingestion/extract_load.py](src/ingestion/extract_load.py)
- Bronze layer notebook — [databricks_ui/bronze_layer.py](databricks_ui/bronze_layer.py)
- dbt models — [dbt_transformations/models/](dbt_transformations/models/)
- Reverse ETL — [src/downstream/lakehouse_to_sheets.py](src/downstream/lakehouse_to_sheets.py)
- Stakeholder context — [docs/business_questions.md](docs/business_questions.md)

---

## Architecture

```
Fraud dataset CSV (Google Drive)
    │
    ▼ src/ingestion/extract_load.py
AWS S3 — banking-lakehouse/raw_data/
    │
    ▼ databricks_ui/bronze_layer.py
Databricks Unity Catalog — bronze.raw_transactions (Delta)
    │
    ▼ dbt staging (incremental merge on surrogate key)
stg_transactions
    ├── sender_balance_error    delta between expected and actual balance movement
    ├── is_zero_impact_txn      sender balance unchanged despite non-zero amount
    └── risk_level              HIGH_RISK if transaction_amount > $10k
    │
    ├── accounts_snapshot (dbt SCD2 snapshot)
    │       Writes a new row whenever risk_level changes for any account
    │
    ├── dim_customers           SCD2 view: valid_from / valid_to risk windows
    ├── fct_transaction         Transaction facts joined with risk dimension
    └── mart_fraud_dashboard    One Big Table — pre-joined for Metabase / BI tools
    │
    ▼ src/downstream/lakehouse_to_sheets.py
Google Sheets — fraud analyst queue (deduplicated by transaction_id)
```

## Stakeholder Questions Answered

| Stakeholder | Question | Solution |
| :--- | :--- | :--- |
| Compliance Officer | Did high-risk accounts move >$10k while their risk flag was active? | `dim_customers` SCD2 + time-travel join on `valid_from` / `valid_to` |
| Fraud Operations | Which transactions today look suspicious for immediate review? | `mart_fraud_dashboard WHERE is_fraud = TRUE` → Google Sheets queue |
| VP of Risk | Cash Out vs. Transfer fraud trends? Are automated flags accurate? | `mart_fraud_dashboard` aggregates in Metabase |

---

## Setup

### Prerequisites

- Databricks workspace with Unity Catalog enabled
- AWS S3 bucket for the landing zone
- Google Drive folder containing the fraud detection CSV
- Google Service Account with Drive (read) and Sheets (write) scopes

### 1) Configure environment

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `GOOGLE_CREDENTIALS_PATH` | Path to the Google service account JSON key file |
| `GOOGLE_DRIVE_FOLDER_ID` | Google Drive folder ID containing the source CSV |
| `DOWNLOAD_PATH` | Local path for the temporary downloaded file |
| `S3_LANDING_BUCKET` | AWS S3 bucket name for the raw landing zone |
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |

### 2) Run ingestion

Downloads the dataset from Google Drive, uploads to S3, then removes the local copy.

```bash
pip install -r requirements.txt
python src/ingestion/extract_load.py
```

### 3) Run the Bronze layer

Open `databricks_ui/bronze_layer.py` in a Databricks notebook session and run all cells to land the S3 data into the Unity Catalog Bronze Delta table.

### 4) Run dbt transformations

```bash
cd dbt_transformations
dbt deps

# Snapshot must run before dim_customers — SCD2 depends on it being current
dbt snapshot

dbt run
dbt test
```

### 5) Push fraud records to Google Sheets

`src/downstream/lakehouse_to_sheets.py` runs as a Databricks notebook (uses `dbutils` and `spark`). Before running, configure the secret scope:

```bash
databricks secrets create-scope my-secrets
databricks secrets put-secret my-secrets google-auth \
  --string-value '<YOUR_GOOGLE_SERVICE_ACCOUNT_JSON>'
```

---

## Project Layout

```
banking-lakehouse/
├── src/
│   ├── ingestion/
│   │   └── extract_load.py          ← Google Drive → S3
│   └── downstream/
│       └── lakehouse_to_sheets.py   ← Gold mart → Google Sheets (deduped)
│
├── databricks_ui/
│   └── bronze_layer.py              ← S3 → Bronze Delta table (notebook)
│
├── dbt_transformations/
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_transactions.sql    ← Incremental merge · ML features
│   │   └── marts/
│   │       ├── dim_customers.sql        ← SCD2 view over accounts_snapshot
│   │       ├── fct_transaction.sql      ← Transaction facts
│   │       └── mart_fraud_dashboard.sql ← OBT for BI tools
│   ├── snapshots/
│   │   └── accounts_snapshot.sql    ← SCD2 snapshot keyed on account_natural_key
│   └── dbt_project.yml
│
├── docs/
│   └── business_questions.md        ← Stakeholder questions and how each is solved
│
└── databricks.yml                   ← Databricks Asset Bundle configuration
```

---

## Notes

- **Snapshot ordering:** Always run `dbt snapshot` before `dbt run`. The `dim_customers` view reads directly from the `accounts_snapshot` table — skipping the snapshot means the SCD2 windows won't reflect the latest risk flag changes.
- **SCD2 time-travel join:** The compliance audit pattern joins `fct_transaction.transaction_timestamp BETWEEN dim_customers.valid_from AND COALESCE(dim_customers.valid_to, CURRENT_TIMESTAMP)` — this reconstructs which risk tier the account held at the exact moment of each transaction, not just its current state.
- **is_zero_impact_txn:** Flags transactions where `sender_old_balance = sender_new_balance` despite a positive `transaction_amount` — a strong fraud indicator in the PaySim dataset, representing a synthetic injection without real balance movement.
- **Google Sheets deduplication:** `lakehouse_to_sheets.py` reads existing `transaction_id` values from the sheet before appending, making reruns safe — no duplicate rows are written.
