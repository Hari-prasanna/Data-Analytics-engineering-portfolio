# Data & Analytics Engineering Portfolio

End-to-end projects spanning cloud lakehouse architecture, real-time analytics, and modern ELT pipelines. Directories are prefixed `MM-YYYY` reflecting when each project was built.

---

## Projects

| Started | Project | Stack | Highlights |
| :---: | :--- | :--- | :--- |
| Apr 2026 | [Banking Fraud Detection Lakehouse](./04-2026-banking-fraud-lakehouse) | Databricks · Delta Lake · dbt (SCD2 · snapshots) · Python · AWS S3 | SCD Type 2 risk dimension · ML fraud features · Reverse ETL to analyst queue |
| Mar 2026 | [Shopstream Clickstream Pipeline](./03-2026-shopstream-pipeline) | PySpark · AWS S3 · Databricks Unity Catalog · Delta Lake · dbt · GitHub Actions | Medallion architecture · Incremental models · Dynamic Data Masking · ZORDER |
| Mar 2026 | [TMDB Analytics Engine](./03-2026-tmdb-elt-pipeline) | AWS S3 · Databricks · dbt · Apache Airflow · GitHub Actions | OOM-proof BytesIO streaming · Dockerized Airflow · [Live dbt Docs](https://hari-prasanna.github.io/Data-Analytics-engineering-portfolio/#!/overview) |
| Mar 2026 | [Airflow Orchestration](./03-2026-airflow-orchestration) | Apache Airflow · Docker · Astronomer CLI | Centralized DAG management · Clean-room venv isolation between tasks |
| Mar 2026 | [LUU Returns Pipeline](./03-2026-luu-returns-pipeline) | Python · Faker · PostgreSQL (Docker) · dbt | Simulated logistics data with injected anomalies · Star schema · Automated dbt tests |
| Mar 2026 | [Weather ELT Pipeline](./03-2026-weather-elt-pipeline) | Python · PostgreSQL · dbt · Bash · Cron | Fully autonomous local pipeline · Zero-touch `@reboot` cron |

---

## Stack at a Glance

| Domain | Tools |
| :--- | :--- |
| Cloud | AWS S3 · IAM · Databricks (Unity Catalog · Delta Lake · DABs · Serverless) |
| Transformation | dbt (incremental · snapshots · SCD2 · tests) · PySpark · SQL |
| Orchestration | Apache Airflow (Dockerized) · Databricks Workflows · GitHub Actions |
| Databases | PostgreSQL · Delta Lake · Oracle |
| Visualization | Grafana · Looker Studio · Metabase · Google Sheets |
| Languages | Python (Pandas · SQLAlchemy · Faker · boto3 · gspread) · SQL · Bash |
