# Standard imports
from datetime import datetime, timedelta
# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator


# Globals
default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}


# Python callable
def greet(ti):
    first_name = ti.xcom_pull(task_ids='task_2', key='first_name')
    last_name = ti.xcom_pull(task_ids='task_2', key='last_name')
    age = ti.xcom_pull(task_ids='task_3', key='age')
    print(f'Hello {first_name} {last_name}, you are {age} years old!')


def get_name(ti):
    ti.xcom_push(key='first_name', value='John')
    ti.xcom_push(key='last_name', value='Doe')


def get_age(ti):
    ti.xcom_push(key='age', value=25)


# DAG definition
with DAG(
    dag_id='python_dag_v6',
    description='Python DAG with a single',
    start_date=datetime(2024, 9, 25, 2),
    schedule_interval='@daily',
) as dag:
    
    task_1 = PythonOperator(
        task_id='task_1',
        python_callable=greet,
    )

    task_2 = PythonOperator(
        task_id='task_2',
        python_callable=get_name,
    )

    task_3 = PythonOperator(
        task_id='task_3',
        python_callable=get_age,
    )

    [task_2, task_3] >> task_1