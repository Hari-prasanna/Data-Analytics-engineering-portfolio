# Movie Data Transformation — dbt (Postgres)

dbt project for the V1 local pipeline. Reads raw TMDB data from the `public` schema in a local PostgreSQL database and builds a dimensional Star Schema (staging → marts).

---

## Models

| Layer | Model | What it does |
|---|---|---|
| Staging | `stg_movies` | Casts raw columns, strips nulls, normalizes string fields |
| Staging | `stg_financials` | Cleans budget/revenue data, filters rows with no financial records |
| Marts | `dim_movies` | Conformed movie dimension with genre and language breakdowns |
| Marts | `fct_financials` | Fact table joining movie and financial data for ROI analysis |

---

## Running

Activate the project virtual environment first:

```bash
cd TMDB-ELT
source venv/bin/activate
cd Movie_data_transformation
```

| Command | What it does |
|---|---|
| `dbt debug` | Verify Postgres connection |
| `dbt run` | Build all models |
| `dbt test` | Run data quality tests |
| `dbt build` | Run + test in one step |

Postgres credentials are read from `~/.dbt/profiles.yml`. See the [parent README](../README.md) for `.env` setup and running the Python extraction step first.
