from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

# 1. Define the Manager's Rules (Default Arguments)
default_args = {
    'owner': 'hari-prasanna',
    'retries': 1, # If a task fails, try it 1 more time before giving up
    'retry_delay': timedelta(minutes=5),
}

# 2. Create the Clipboard (The DAG itself)
with DAG(
    dag_id='hello_portfolio_pipeline', 
    default_args=default_args,
    description='My very first Airflow DAG',
    start_date=datetime(2023, 1, 1), 
    schedule='@daily',            
    catchup=False                    
) as dag:

    # Worker 1: Tests the tunnel to make sure it can see the files
    task_1 = BashOperator(
        task_id='verify_tunnel',
        bash_command='ls -la /usr/local/airflow/include/TMDB-ELT'
    )

    # Worker 2: The Enterprise Python Clean Room
    task_2 = BashOperator(
        task_id='run_tmdb_python_elt',
        bash_command='''
        cd /usr/local/airflow/include/TMDB-ELT && \
        rm -rf /tmp/tmdb_env && \
        python -m venv /tmp/tmdb_env && \
        source /tmp/tmdb_env/bin/activate && \
        unset PIP_CONSTRAINT && \
        pip install -r requirements_python.txt && \
        python load_movies.py && \
        deactivate && \
        rm -rf /tmp/tmdb_env
        '''
    )
# Worker 3: The Enterprise dbt Clean Room
    task_3 = BashOperator(
        task_id='run_dbt_models',
        bash_command='''
        # 0. THE FIX: Demolish any leftover ghost rooms from previous crashes
        rm -rf /tmp/dbt_env /tmp/.env_clean /tmp/dbt_project
        
        # 1. Stop on error
        set -e
        
        # 2. Clean passwords
        cp /usr/local/airflow/include/TMDB-ELT/.env /tmp/.env_clean
        sed -i 's/\\r$//' /tmp/.env_clean
        
        # 3. Load passwords
        set -a
        source /tmp/.env_clean
        set +a
        
        # 4. Copy the entire dbt project to the Public Park
        cp -r /usr/local/airflow/include/TMDB-ELT/Movie_data_transformation /tmp/dbt_project
        
        # 5. Build Clean Room
        python -m venv /tmp/dbt_env
        source /tmp/dbt_env/bin/activate
        
        # 6. Install dbt silently
        pip install -q -r /usr/local/airflow/include/TMDB-ELT/requirements_dbt.txt
        
        # 7. Run dbt in the Public Park!
        cd /tmp/dbt_project
        dbt build --full-refresh --profiles-dir .
        
        # 8. Clean up
        deactivate
        rm -rf /tmp/dbt_env /tmp/.env_clean /tmp/dbt_project
        '''
    )
    # 4. Set the Order of Operations (The DAG Arrows)
    # This tells the Manager: Run Task 1, THEN Task 2, THEN Task 3
    task_1 >> task_2 >> task_3