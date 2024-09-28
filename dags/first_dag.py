# Standard imports
from datetime import datetime, timedelta
# Airflow imports
from airflow import DAG
from airflow.operators.bash import BashOperator


# Globals
default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}


# DAG definition
with DAG(
    dag_id='first_dag_v3',
    description='My first DAG',
    start_date=datetime(2024, 9, 25, 2),
    schedule_interval='@daily',
) as dag:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='echo "Hello World"',
    )

    task_2 = BashOperator(
        task_id='task_2',
        bash_command='echo "Second task"',
    )

    task_3 = BashOperator(
        task_id='task_3',
        bash_command='echo "Third task"',
    )

    task_1.set_downstream(task_2)
    task_1.set_downstream(task_3)