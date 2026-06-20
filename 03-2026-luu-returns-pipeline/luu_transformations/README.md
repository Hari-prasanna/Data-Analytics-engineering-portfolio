# LUU Returns Transformations — dbt (Postgres)

dbt project for the Zalando LUU Returns Pipeline. Reads raw logistics data from the `raw` schema in a Dockerized PostgreSQL database and builds a Star Schema using a Medallion Architecture (raw → staging → marts).

---

## Models

| Layer | Model | What it does |
|---|---|---|
| Staging (Silver) | `stg_inbound_packages` | View — casts types, normalizes strings, nullifies logical timestamp errors, deduplicates re-scanned items |
| Marts (Gold) | `dim_load_carriers` | Pallet dimension — one row per pallet with `total_items` and `total_weight_kg` aggregates |
| Marts (Gold) | `fact_processed_items` | Item fact table — tracks quality grade and routing per item, FK to `dim_load_carriers` |

---

## Running

Ensure the Dockerized Postgres is running first (`docker-compose up -d` from the parent directory), then:

```bash
cd personal-projects/luu-returns-pipeline/luu_transformations

dbt debug            # Verify database connection

dbt run              # Build staging views (dev target)
dbt run --target prod  # Build Gold physical tables
dbt test --target prod # PK uniqueness, FK integrity, not-null, accepted values
```

See the [parent README](../README.md) for the full local setup, Docker infrastructure start, and data generation steps that must run before dbt.
