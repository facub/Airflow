# Standard imports
from datetime import datetime, timedelta
# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


# Globals
default_args = {
    'owner': 'airflow',
    'retries': 6,
    'retry_delay': timedelta(minutes=5),
}


# DAG definition
with DAG(
    dag_id='dag_with_catchup_and_backfill_v2',
    default_args=default_args,
    start_date=datetime(2024, 9, 20),
    schedule_interval='@daily',
    catchup=False,
) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo This is a simple bash command',
    )
