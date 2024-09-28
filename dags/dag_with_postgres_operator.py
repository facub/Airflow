# Standard imports
from datetime import datetime, timedelta
# Airflow imports
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


# Globals
default_args = {
    'owner': 'airflow',
    'retries': 6,
    'retry_delay': timedelta(minutes=5),
}


# DAG definition
with DAG(
    dag_id='dag_with_postgres_operator_v3',
    default_args=default_args,
    start_date=datetime(2024, 9, 28),
    schedule_interval='@daily',
) as dag:
    task_1 = PostgresOperator(
        task_id='task_1',
        postgres_conn_id='postgres_localhost',
        sql='''CREATE TABLE IF NOT EXISTS dag_runs (
            dt DATE,
            dag_id CHARACTER VARYING,
            PRIMARY KEY (dt, dag_id)
        )'''
    )

    task2 = PostgresOperator(
        task_id='task_2',
        postgres_conn_id='postgres_localhost',
        sql="""
            INSERT INTO dag_runs (dt, dag_id) VALUES ('{{ ds }}', '{{ dag.dag_id }}')
        """
    )

    task3 = PostgresOperator(
        task_id='task_3',
        postgres_conn_id='postgres_localhost',
        sql="""
            DELETE FROM dag_runs WHERE dt = '{{ ds }}' AND dag_id = '{{ dag.dag_id }}';
        """
    )

    task_1 >> task3 >> task2
