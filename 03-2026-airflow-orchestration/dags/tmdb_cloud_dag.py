from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

# 1. Define the Manager's Rules
default_args = {
    'owner': 'hari-prasanna',
    'retries': 1, 
    'retry_delay': timedelta(minutes=5),
}

# 2. Create the Clipboard (The DAG itself)
with DAG(
    dag_id='tmdb_enterprise_cloud_pipeline', 
    default_args=default_args,
    description='Orchestrates the TMDB to AWS S3 and Databricks pipeline',
    start_date=datetime(2026, 3, 1), 
    schedule='@daily',            
    catchup=False                    
) as dag:

    # Worker 1: Tests the tunnel to make sure it can see the new cloud folders
    task_1 = BashOperator(
        task_id='verify_tunnel',
        bash_command='ls -la /usr/local/airflow/include/TMDB-ELT/cloud_pipeline'
    )

    # Worker 2: The AWS S3 Extraction Clean Room
    task_2 = BashOperator(
        task_id='extract_to_aws_s3',
        bash_command='''
        # 1. Prepare passwords securely from the .env file
        cp /usr/local/airflow/include/TMDB-ELT/.env /tmp/.env_clean
        sed -i 's/\\r$//' /tmp/.env_clean
        set -a; source /tmp/.env_clean; set +a
        
        # 2. Build the Clean Room
        cd /usr/local/airflow/include/TMDB-ELT/cloud_pipeline
        rm -rf /tmp/s3_env
        python -m venv /tmp/s3_env
        source /tmp/s3_env/bin/activate
        unset PIP_CONSTRAINT
        
        # 3. Install Cloud Dependencies
        pip install -q pandas requests boto3 python-dotenv
        
        # 4. Run the Extraction!
        python extract_to_s3.py
        
        # 5. Clean up
        deactivate
        rm -rf /tmp/s3_env /tmp/.env_clean
        '''
    )

    # Worker 3: The Databricks dbt Clean Room
    task_3 = BashOperator(
        task_id='run_databricks_dbt',
        bash_command='''
        # 1. Prepare passwords securely from the .env file
        cp /usr/local/airflow/include/TMDB-ELT/.env /tmp/.env_clean
        sed -i 's/\\r$//' /tmp/.env_clean
        set -a; source /tmp/.env_clean; set +a
        
        # 2. Build the Clean Room
        cd /usr/local/airflow/include/TMDB-ELT/cloud_pipeline/databricks_cloud
        rm -rf /tmp/dbt_env
        python -m venv /tmp/dbt_env
        source /tmp/dbt_env/bin/activate
        unset PIP_CONSTRAINT
        
        # 3. Install the Databricks adapter
        pip install -q dbt-databricks
        
        # 4. Run dbt against the Cloud!
        dbt deps --profiles-dir .
        dbt build --profiles-dir .
        
        # 5. Clean up
        deactivate
        rm -rf /tmp/dbt_env /tmp/.env_clean
        '''
    )

    # 4. Set the Order of Operations
    task_1 >> task_2 >> task_3