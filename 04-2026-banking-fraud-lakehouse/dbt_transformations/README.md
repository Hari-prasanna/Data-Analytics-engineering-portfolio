# Banking Lakehouse dbt Project

dbt project for the Banking Fraud Detection Lakehouse. Reads from the Databricks Unity Catalog Bronze layer and builds the fraud analysis dimensional model, including an SCD Type 2 customer risk dimension backed by a dbt snapshot.

---

## Models

| Layer | Model | What it does |
|---|---|---|
| Staging | `stg_transactions` | Incremental merge on surrogate key · Adds ML features: `sender_balance_error`, `is_zero_impact_txn`, `risk_level` |
| Snapshot | `accounts_snapshot` | SCD2 snapshot — writes a new row whenever `risk_level` changes for any account |
| Marts | `dim_customers` | SCD2 view over the snapshot, exposes `valid_from` / `valid_to` risk windows |
| Marts | `fct_transaction` | Transaction facts joined with the risk dimension |
| Marts | `mart_fraud_dashboard` | One Big Table — pre-joined for Metabase and Google Sheets downstream |

---

## Running

```bash
cd banking-lakehouse/dbt_transformations

dbt deps

# Snapshot must run first — dim_customers is a view over accounts_snapshot
dbt snapshot

dbt run
dbt test
```

See the [parent README](../README.md) for full environment setup, the required AWS and Google credentials, and the Databricks secrets configuration needed for the downstream Google Sheets step.
