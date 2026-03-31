# 👨‍💻 Data & Analytics Engineering Portfolio

End-to-end projects spanning **production automation**, **cloud lakehouse architecture**, **real-time dashboarding**, and **modern ELT pipelines**.

---

## 🏢 Work Projects — Production Systems

Pipelines running in production at a warehouse facility in Ludwigsfelde, Germany.

| Project | Tech | Impact |
| :--- | :--- | :--- |
| [🚀 Oracle to Google Sheets: ETL Pipeline](./work-related/oracle-sheets-looker-etl) | Python, Pandas, SQLAlchemy, Databricks Workflows, Google Chat Cards V2 | **100 → <10 min/day** manual effort · Powers the [DG Monitor Dashboard](https://github.com/Hari-prasanna/BI-Tools-Projects/blob/main/LUU-DG-Monitor/README.md) |
| [📊 Internal Transport: Real-Time KPI Dashboard](./work-related/internal-transport-kpi-dashboard) | Python, SQLAlchemy, Databricks, Grafana, Google Sheets API | **Saved €10K** vs vendor · Runs at **<€70/month** · Zero-credential TV monitors on warehouse floor |

---

## 🛠️ Personal Projects

| Project | Tech | Highlights |
| :--- | :--- | :--- |
| [🛒 Shopstream: Clickstream Lakehouse](./clickstream-conversion-pipeline) | PySpark, AWS S3, Databricks Unity Catalog, Delta Lake, dbt, GitHub Actions | Medallion Architecture · Incremental processing · Dynamic Data Masking · ZORDER optimization |
| [🎬 TMDB: Local to Cloud Lakehouse](./TMDB-ELT) | AWS S3, Databricks, dbt, Apache Airflow, GitHub Actions | OOM-proof `BytesIO` streaming to S3 · Dockerized Airflow · CI/CD with path-filtering — [Live dbt Docs](https://hari-prasanna.github.io/Data-Analytics-engineering-portfolio/#!/overview) |
| [📦 Zalando LUU Returns (Mock ELT)](./zalando-luu-returns-pipeline) | Python, Faker, PostgreSQL (Docker), dbt | Simulated logistics data with injected anomalies · Star Schema · Automated dbt quality tests |
| [🎵 Airflow Orchestration](./orchestration) | Apache Airflow, Docker, Python | Centralized DAG management for TMDB pipeline · "Clean Room" env isolation |
| [⛅ Weather ELT Pipeline](./personal-projects/weather-elt-pipeline) | Python, PostgreSQL, dbt, Bash, Cron | Fully autonomous local pipeline · Zero-touch `@reboot` Cron automation |
