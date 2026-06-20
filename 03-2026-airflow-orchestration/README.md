# TMDB Pipeline Orchestration

Dockerized Apache Airflow environment (Astronomer Runtime) managing DAG execution for the TMDB Analytics Engine. Pipeline source code lives in `include/TMDB-ELT/` and is mounted into the container at runtime — each task spins up an isolated virtual environment (clean-room pattern) to avoid dependency conflicts between Airflow and the pipeline libraries.

- V1 local Postgres DAG — [dags/TMDB_ELT.py](dags/TMDB_ELT.py)
- V2 cloud (S3 + Databricks) DAG — [dags/tmdb_cloud_dag.py](dags/tmdb_cloud_dag.py)

---

## DAGs

### `hello_portfolio_pipeline` — `dags/TMDB_ELT.py`

Orchestrates the V1 local Postgres pipeline on a daily schedule.

| Task | What it does |
|---|---|
| `verify_tunnel` | Confirms the `include/` mount is visible inside the container |
| `run_tmdb_python_elt` | Creates `/tmp/tmdb_env`, installs deps, runs `load_movies.py`, tears down env |
| `run_dbt_models` | Creates `/tmp/dbt_env`, copies `.env`, runs `dbt build` against Postgres, tears down env |

Task 2 and 3 run sequentially. If the Python ELT fails, dbt does not run.

### `tmdb_cloud_dag.py`

Orchestrates the V2 cloud pipeline: Python extraction to S3, followed by Databricks dbt transformations.

---

## Local Setup

### Prerequisites

- Docker Desktop running
- Astronomer CLI (`brew install astro`)

### 1) Start Airflow

```bash
astro dev start
```

Starts five containers: Postgres (metadata DB), Scheduler, DAG Processor, API Server, and Triggerer. The Airflow UI is available at [http://localhost:8080](http://localhost:8080) — default credentials `admin` / `admin`.

### 2) Configure the Postgres connection (V1 DAG)

Add the connection in Airflow UI under **Admin → Connections**, or set it in [airflow_settings.yaml](airflow_settings.yaml) before starting:

| Field | Value |
|---|---|
| Connection ID | `postgres_default` |
| Host | `host.docker.internal` |
| Port | `5432` |
| Database | `postgres` |
| Login | `postgres` |

### 3) Trigger a DAG run

Unpause the DAG in the UI or trigger it manually via the CLI:

```bash
astro dev run dags trigger hello_portfolio_pipeline
```

### 4) Stop Airflow

```bash
astro dev stop
```

---

## Project Layout

```
orchestration/
├── dags/
│   ├── TMDB_ELT.py          ← Daily DAG: Python ELT → dbt → Postgres (V1)
│   └── tmdb_cloud_dag.py    ← Cloud DAG: Python extract → S3 → Databricks (V2)
│
├── include/
│   └── TMDB-ELT/            ← Pipeline source files, mounted into the container
│
├── Dockerfile               ← Astro Runtime base image
├── requirements.txt         ← Python packages installed in the Airflow environment
├── packages.txt             ← OS-level packages
└── airflow_settings.yaml    ← Local connections, variables, and pools
```

---

## Notes

- **Clean-room venv pattern:** Each BashOperator task creates a fresh `/tmp/` virtual environment, installs only what it needs, runs the script, then removes the env. This ensures Airflow's own Python environment never conflicts with the pipeline's dependencies (e.g. different `dbt-core` versions).
- **Port conflicts:** Airflow requires ports 8080 (UI) and 5432 (Postgres). If those ports are occupied, stop the conflicting service or update port mappings in the Astronomer project config before running `astro dev start`.
- **include/ symlink:** The `include/TMDB-ELT/` directory is a copy of the TMDB project. If you update the pipeline code in the root `TMDB-ELT/` folder, sync the changes into `include/` before triggering a DAG run.
