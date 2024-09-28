# Standard imports
from datetime import datetime, timedelta
# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator


# Globals
default_args = {
    'owner': 'airflow',
    'retries': 6,
    'retry_delay': timedelta(minutes=5),
}


def get_sklearn():
    import sklearn
    print(f'Sklearn version: {sklearn.__version__}')


def get_matplotlib():
    import matplotlib
    print(f'Matplotlib version: {matplotlib.__version__}')

# DAG definition
with DAG(
    dag_id='dag_with_python_dependecies_v2',
    default_args=default_args,
    start_date=datetime(2024, 9, 28),
    schedule_interval='@daily',
) as dag:
    
    task_1 = PythonOperator(
        task_id='task_1',
        python_callable=get_sklearn,
    )

    task_2 = PythonOperator(
        task_id='task_2',
        python_callable=get_matplotlib,
    )

    task_1 >> task_2