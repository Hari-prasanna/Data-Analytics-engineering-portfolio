# 👨‍💻 Data | Analytics Engineering Project Portfolio

Welcome to my portfolio! Here you will find end-to-end data and analytics engineering projects focused on automation, cloud integration, modern data lakehouse architecture, and efficient ELT pipelines.

---

## 🏢 Work-Related Projects

### 1. [Oracle to Google Sheets Automation](./work-related/oracle-sheets-looker-etl)
* **Tech:** PySpark, Databricks, Oracle SQL, Google Sheets API.
* **Summary:** Automated a critical inventory reporting process, reducing manual work from 100 mins/day to <10 min.
* **Key Skills:** Data Extraction, Cloud Scheduling, Alerting, Process Automation.

---

## 🛠️ Personal Projects

### 1. [Enterprise E-Commerce Clickstream Lakehouse](./clickstream-conversion-pipeline) *(In Progress)*
* **Tech:** Python 3.11, PySpark, Databricks Unity Catalog, dbt, GitHub Actions.
* **Summary:** An enterprise-grade pipeline that extracts entities from a raw JSON/CSV event firehose, handles Slowly Changing Dimensions (SCD Type 2) for dynamic pricing, and builds a highly-optimized Kimball Star Schema.
* **Key Skills:** Dimensional Data Modeling, PySpark Entity Extraction, dbt, CI/CD, Advanced SQL (Window Functions).

### 2. [TMDB Cloud Data Lakehouse Pipeline](./TMDB-ELT)
* **Tech:** Python, AWS S3, Databricks, dbt, GitHub Actions.
* **Summary:** Modernized a local ETL pipeline into a scalable Cloud Data Lakehouse. Extracts API data to an AWS S3 data lake and utilizes Databricks compute to transform the raw data into business-ready Gold tables via dbt.
* **Key Skills:** Cloud Architecture, Decoupled Compute/Storage, GitHub Secrets Management, dbt Data Contracts.

### 3. [Apache Airflow Orchestration](./orchestration)
* **Tech:** Apache Airflow, Docker, Python.
* **Summary:** Centralized orchestration repository managing the DAGs for the TMDB cloud data pipeline. Utilizes a "Clean Room" strategy via Airflow `BashOperators` to isolate Python virtual environments and prevent dependency conflicts during runtime.
* **Key Skills:** Workflow Orchestration, DAG Design, Dependency Management, Containerized Execution.

### 4. [Weather ELT Pipeline & dbt Transformations](./personal-projects/weather-elt-pipeline)
* **Tech:** Python, PostgreSQL, dbt, Bash, Unix Cron.
* **Summary:** Engineered a fully autonomous ELT pipeline that extracts daily API weather data, loads it into a local PostgreSQL warehouse, and transforms it into analytical tables using dbt.
* **Key Skills:** API Integration, Data Modeling (dbt), Environment Management, Background Orchestration (Cron).
