# Zalando LUU Returns Logistics Pipeline (Mock ELT)

End-to-end ELT pipeline simulating Zalando's Local Utility Unit (LUU) returns logistics network. The data generator produces complex, hierarchical mock logistics data (items packed inside pallets), deliberately injecting real-world warehouse scanner anomalies — negative weights, logical timestamp errors, and duplicate scans. dbt cleanses and models the data into a production-ready Star Schema using a Medallion Architecture.

- Data generator — [luu_returns_generator.py](luu_returns_generator.py)
- Raw loader — [load_data.py](load_data.py)
- dbt project — [luu_transformations/](luu_transformations/)
- Docker infrastructure — [docker-compose.yml](docker-compose.yml)

---

## Architecture

```
Faker-generated mock logistics data
    │
    ▼ luu_returns_generator.py  (injected anomalies: negatives, timestamp errors, duplicates)
CSV files
    │
    ▼ load_data.py  (SQLAlchemy → raw schema)
Dockerized PostgreSQL — raw.inbound_packages
    │
    ▼ dbt staging (view)
stg_inbound_packages  — type casts · string normalization · deduplication · null out timestamp errors
    │
    ▼ dbt marts (physical tables)
    ├── dim_load_carriers   ← One row per pallet (total_items, total_weight_kg)
    └── fact_processed_items ← One row per item (quality grade, routing, FK to dim_load_carriers)
```

## Injected Data Anomalies

| Anomaly | How it's modeled |
| :--- | :--- |
| Negative package weights | `CASE WHEN weight_kg < 0 THEN NULL` in staging |
| Scanner re-scans (duplicates) | `ROW_NUMBER()` deduplication in staging view |
| Logical timestamp errors (arrival before departure) | Nullified in staging; flagged in dbt test |

---

## Setup

### Prerequisites

- Docker Desktop running
- Python 3.8+

### 1) Configure environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pandas sqlalchemy psycopg2-binary faker python-dotenv dbt-core dbt-postgres

cp .env.example .env
```

### 2) Start infrastructure

```bash
docker-compose up -d
```

Postgres maps to port `5433` to avoid conflicts with any locally running Postgres on the default `5432`.

### 3) Generate and load data

```bash
python luu_returns_generator.py
python load_data.py
```

### 4) Run dbt transformations

```bash
cd luu_transformations

dbt debug          # Verify connection to Dockerized Postgres

dbt run            # Build staging views (dev target)
dbt run --target prod   # Build Gold physical tables in the marts schema
dbt test --target prod  # PK uniqueness · FK integrity · not-null · accepted values
```

---

## Project Layout

```
luu-returns-pipeline/
├── luu_returns_generator.py          ← Faker-based data generator with injected anomalies
├── load_data.py              ← CSV → raw.inbound_packages (SQLAlchemy)
├── docker-compose.yml        ← Isolated Postgres on port 5433
│
├── luu_transformations/      ← dbt project
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_inbound_packages.sql ← Silver: cleanse and deduplicate
│   │   └── marts/
│   │       ├── dim_load_carriers.sql    ← Pallet dimension
│   │       └── fact_processed_items.sql ← Item fact table
│   └── dbt_project.yml
│
└── .env.example
```

---

## Notes

- **Port 5433:** Docker maps the container Postgres to `5433` instead of the default `5432`. Update your `~/.dbt/profiles.yml` to use `port: 5433` for this project.
- **Anomaly injection intent:** The generator deliberately creates bad data to prove the staging layer catches it. After `dbt run --target prod`, `fact_processed_items` should contain zero negative weights and zero duplicate item scans — the dbt tests enforce this.
- **Star schema FK enforcement:** dbt `relationship` tests verify every `fact_processed_items.load_carrier_id` has a matching row in `dim_load_carriers`. If the generator creates orphaned items, the test will fail before the marts table is promoted.
