# Standard imports
from datetime import datetime, timedelta
# Airflow imports
from airflow import DAG
from airflow.operators.bash import BashOperator


# Globals
default_args = {
    'owner': 'airflow',
    'retries': 6,
    'retry_delay': timedelta(minutes=5),
}


# DAG definition
with DAG(
    dag_id='dag_with_cron_expression_v4',
    default_args=default_args,
    start_date=datetime(2024, 9, 20),
    schedule_interval='0 3 * * Tue-Sat',
) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo This is a simple bash command'
    )
