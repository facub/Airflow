# Standard imports
import csv
import logging
from datetime import datetime, timedelta
# Extra imports
from tempfile import NamedTemporaryFile
# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


# Globals
default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}


# Function to extract data from Postgres and save it to a file
def postgres_to_s3(ds_nodash, next_ds_nodash):
    # Create a PostgresHook instance
    hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE date >= %s AND date < %s", (ds_nodash, next_ds_nodash))
    logging.info(f'Extracting data from Postgres for {ds_nodash} and {next_ds_nodash}')
    with NamedTemporaryFile(mode='w', suffix=f"{ds_nodash}.txt") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info(f'Data extracted from Postgres and saved to get_orders_{ds_nodash}.txt')
        # Create an S3Hook instance
        s3_hook = S3Hook(aws_conn_id='minio_conn')
        s3_hook.load_file(
            filename=f.name,
            key=f'orders/{ds_nodash}.txt',
            bucket_name='airflow',
        )
        logging.info(f'File {f.name} uploaded to S3')


# DAG definition
with DAG(
    dag_id='dag_with_postgres_hooks_v4',
    default_args=default_args,
    start_date=datetime(2024, 9, 26),
    schedule_interval='@daily'
) as dag:

    task_1 = PythonOperator(
        task_id='task_1',
        python_callable=postgres_to_s3,
    )

    task_1