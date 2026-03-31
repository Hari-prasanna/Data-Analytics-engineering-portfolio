# 👨‍💻 Data & Analytics Engineering Portfolio

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Airflow-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)

Welcome! This repository contains end-to-end **Data and Analytics Engineering** projects spanning production automation, cloud lakehouse architecture, real-time dashboarding, and modern ELT pipelines.

---

## 🏢 Work Projects — Production Systems

Real-world pipelines running in production at a warehouse facility in Ludwigsfelde (LUU), solving tangible operational problems.

### 1. [🚀 Oracle to Google Sheets: ETL Pipeline](./work-related/oracle-sheets-looker-etl)

> Automated a critical inventory reporting process, cutting daily manual effort from **100 minutes to under 10**.

| | |
| :--- | :--- |
| **Tech** | Python, Pandas, SQLAlchemy, Databricks Workflows, Google Sheets API, Google Chat Cards V2 |
| **Highlights** | Query pushdown to Oracle via parameterized SQL · Multi-task orchestration with `dbutils.jobs.taskValues` · Adaptive ChatOps notifications (success dashboard card / failure alert with manual fallback) |
| **Impact** | Powers the [DG Monitor Dashboard](https://github.com/Hari-prasanna/BI-Tools-Projects/blob/main/LUU-DG-Monitor/README.md) — ensures strict 20-Liter dangerous goods threshold compliance |

---

### 2. [📊 Internal Transport: Real-Time KPI Dashboard](./work-related/internal-transport-kpi-dashboard)

> Replaced a €10,000 vendor proposal with an in-house, real-time TV dashboard running at **under €70/month**.

| | |
| :--- | :--- |
| **Tech** | Python, SQLAlchemy, Databricks, Google Sheets API, Self-Hosted Grafana |
| **Highlights** | Zero-maintenance KPI engine (drop a `.sql` file to add a metric) · Cost-optimized compute loop with automated overnight shutdown · Zero-credential TV token streaming to warehouse floor monitors |
| **Impact** | Site leads, team leads, and floor employees gain passive, real-time visibility into open orders and transport volumes — no logins, no walkie-talkies |

---

## 🛠️ Personal Projects — Cloud & Data Engineering

Projects focused on building scalable cloud architectures, data modeling, and modern engineering best practices.

### 1. [🛒 Shopstream: E-Commerce Clickstream Lakehouse](./clickstream-conversion-pipeline)

> Enterprise-grade pipeline turning raw clickstream events into conversion funnel analytics.

| | |
| :--- | :--- |
| **Tech** | Python, PySpark, AWS S3 & IAM, Databricks Unity Catalog, Delta Lake, dbt, GitHub Actions |
| **Highlights** | Medallion Architecture (Bronze → Silver → Gold) · Incremental processing with MD5 surrogate keys · ZORDER clustering & VACUUM optimization · Dynamic Data Masking (DDM) for PII · Service Principals for CI/CD authentication |
| **Key Skills** | Cloud Security (IAM & least-privilege), Dimensional Modeling, Delta Lake Optimization, Data Governance |

---

### 2. [🎬 TMDB Analytics Engine: Local to Cloud Data Lakehouse](./TMDB-ELT)

> Migrated a local Postgres pipeline to an enterprise-grade Cloud Data Lakehouse on AWS + Databricks.

| | |
| :--- | :--- |
| **Tech** | Python, AWS S3, Databricks, Unity Catalog, dbt (`dbt-databricks`, `dbt-postgres`), Apache Airflow, GitHub Actions |
| **Highlights** | OOM-proof ingestion via `io.BytesIO` streaming to S3 · Star Schema modeling across Bronze/Silver/Gold layers · Dockerized Airflow orchestration with "Clean Room" `BashOperator` strategy · CI/CD with monorepo path-filtering |
| **Key Skills** | Cloud Migration, Decoupled Compute/Storage, Workflow Orchestration, GitHub Secrets Management |

> 🔍 [View the Live dbt Data Lineage & Docs](https://hari-prasanna.github.io/Data-Analytics-engineering-portfolio/#!/overview)

---

### 3. [📦 Zalando LUU Returns Logistics Pipeline (Mock ELT)](./zalando-luu-returns-pipeline)

> Simulated a warehouse returns logistics network with deliberately injected data anomalies, modeled into a production-ready Star Schema.

| | |
| :--- | :--- |
| **Tech** | Python, Pandas, Faker, SQLAlchemy, PostgreSQL (Dockerized), dbt |
| **Highlights** | Realistic data generation with intentional anomalies (negative weights, timestamp errors, duplicate scans) · Medallion Architecture: Raw → Staging (cleansed view) → Marts (Star Schema) · Automated dbt tests for PK uniqueness, FK integrity, and accepted values |
| **Key Skills** | Data Quality Engineering, Dimensional Modeling (Star Schema), Docker, dbt Testing |

---

### 4. [🎵 Apache Airflow Orchestration](./orchestration)

> Centralized orchestration layer managing the DAGs for the TMDB cloud pipeline.

| | |
| :--- | :--- |
| **Tech** | Apache Airflow, Docker, Python |
| **Highlights** | "Clean Room" strategy via `BashOperators` to isolate virtual environments · Dependency-aware DAG sequencing (Python extraction → dbt transformation) |
| **Key Skills** | Workflow Orchestration, DAG Design, Containerized Execution |

---

### 5. [⛅ Weather ELT Pipeline](./personal-projects/weather-elt-pipeline)

> A fully autonomous local pipeline that extracts daily weather data for 10 German cities, loads to PostgreSQL, and transforms via dbt — all triggered on boot via Cron.

| | |
| :--- | :--- |
| **Tech** | Python, PostgreSQL, dbt, Bash, Unix Cron |
| **Highlights** | Zero-touch automation (`@reboot` Cron + Bash master script) · Environment isolation with `venv` · Secure credential management via `.env` + `.gitignore` |
| **Key Skills** | API Integration, dbt Modeling, Background Orchestration, Environment Management |
