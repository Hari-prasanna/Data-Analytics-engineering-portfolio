# Cloud Pipeline — dbt (Databricks)

dbt project for the V2 cloud pipeline. Reads from the Databricks Unity Catalog Bronze layer and builds Silver and Gold Delta tables using Databricks Serverless compute.

---

## Models

| Layer | Model | What it does |
|---|---|---|
| Staging (Silver) | `stg_movies` | Casts and deduplicates Bronze records, generates surrogate key |
| Staging (Silver) | `stg_financials` | Cleans financial data, filters rows missing budget or revenue |
| Marts (Gold) | `dim_movies` | Movie dimension with genre and language metadata |
| Marts (Gold) | `fct_financials` | Fact table for ROI and financial performance queries |

---

## Running

Configure `~/.dbt/profiles.yml` with your Databricks workspace credentials, then:

```bash
cd TMDB-ELT/cloud_pipeline/databricks_cloud

dbt deps
dbt build
```

See the [parent README](../../README.md) for the full cloud setup — including AWS credentials, Databricks external location configuration, and the Python extraction step that must run first.
