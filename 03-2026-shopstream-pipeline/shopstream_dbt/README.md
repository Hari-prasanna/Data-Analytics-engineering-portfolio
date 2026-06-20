# Shopstream dbt Project

dbt project for the Shopstream Medallion pipeline. Reads raw clickstream Parquet files from the Databricks Bronze layer and builds Silver and Gold Delta tables in Databricks Unity Catalog.

---

## Models

| Layer | Model | What it does |
|---|---|---|
| Staging (Bronze → Silver) | `stg_events` | Deduplicates raw events, standardizes timestamps, generates md5 surrogate key on `user_session + user_id + product_id + event_type + event_time` |
| Gold | `dim_users` | User dimension derived from distinct session records |
| Gold | `dim_products` | Product dimension from distinct product interactions |
| Gold | `fct_session_funnel` | Conversion funnel fact — tracks View → Cart → Checkout → Purchase per session |

---

## Running

```bash
cd clickstream-conversion-pipeline/shopstream_dbt

dbt deps
dbt run --target dev        # Build Silver staging models
dbt run --target prod       # Build Gold physical Delta tables
dbt test                    # Uniqueness, not-null, and referential integrity checks
```

The Databricks connection is configured in `~/.dbt/profiles.yml`. See the [parent README](../README.md) for environment setup, S3 ingestion, and Unity Catalog configuration.
