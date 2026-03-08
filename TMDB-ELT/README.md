# 🎬 TMDB Analytics Engine: Modern Data Stack Pipeline

An end-to-end ELT pipeline that extracts movie and financial data from the TMDB API, loads it into a PostgreSQL data warehouse, and models it for analytics using dbt. The entire workflow is protected by a custom GitHub Actions CI/CD pipeline.

## 🏗️ Architecture

1. **Extract & Load (Python):** Connects to the TMDB REST API, handles pagination and rate limits, processes the JSON responses via Pandas, and loads the raw data into PostgreSQL.
2. **Transform (dbt):** Cleans and models the raw data into a dimensional Star Schema (e.g., `fact_movie_financials`) for downstream BI tools.
3. **CI/CD (GitHub Actions):** An automated "Traffic Cop" that spins up a temporary Postgres database, runs the Python extraction, and executes `dbt build` to test code integrity on every Pull Request.

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

* **Data Extraction:** Python (Requests API, Pandas)
* **Data Warehouse:** PostgreSQL
* **Data Transformation:** dbt (Data Build Tool)
* **CI/CD & Security:** GitHub Actions, GitHub Environments

## 🧠 What I Learned

Building this project transitioned my skills from writing standalone scripts to architecting enterprise-grade pipelines. Key takeaways include:

* **Enterprise CI/CD:** Designed a GitHub Actions workflow using `paths` filtering to only trigger when specific monorepo files change, saving cloud compute time.
* **Security Best Practices:** Moved away from hardcoded credentials and repository secrets, implementing strict **GitHub Environments** (`tmdb-production`) to isolate database credentials and API keys.
* **Advanced Git Workflow:** Mastered monorepo organization, utilizing `git mv` for keeping commit history, resolving merge conflicts via `git pull --rebase`.
* **Data Modeling:** Built reliable, tested data models using dbt, enforcing data quality rules before the data reaches the presentation layer.

## 🚀 How to Run Locally

1. Clone the repository and navigate to the `TMDB-ELT` folder.
2. Create a `.env` file with your credentials:
   ```text
   TMDB_API_KEY=your_api_key
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_NAME=postgres
   DB_HOST=localhost
   DB_PORT=5432
    ```
3. Install dependencies: pip install -r requirements.txt (or manually install pandas, sqlalchemy, dbt-postgres, etc.).
4. Run the Python extraction: python load_movies.py
5. Run the dbt models: cd Movie_data_transformation && dbt build