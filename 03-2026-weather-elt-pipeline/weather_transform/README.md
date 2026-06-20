# Weather Transform — dbt (Postgres)

dbt project for the Weather ELT Pipeline. Reads raw weather API records from the `public` schema in a local PostgreSQL database and builds cleaned staging and mart tables.

---

## Models

| Layer | Model | What it does |
|---|---|---|
| Staging | `stg_weather` | Casts raw API response fields, normalizes city names, handles null temperature and humidity readings |
| Marts | `fct_weather` | Atomic fact table — one row per city per API call |
| Marts | `fct_weather_daily` | Daily aggregate — average temperature, min/max readings per city |

---

## Running

```bash
cd 06-weather-elt-pipeline/weather_transform

dbt debug     # Verify Postgres connection
dbt build     # Run and test all models
```

Run `el_weather.py` from the parent directory first to populate the raw schema before executing dbt. See the [parent README](../README.md) for full setup including the `.env` configuration and `@reboot` cron automation.
