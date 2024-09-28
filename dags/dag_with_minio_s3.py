# Standard imports
from datetime import datetime, timedelta
# Airflow imports
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


# Globals
default_args = {
    'owner': 'airflow',
    'retries': 6,
    'retry_delay': timedelta(minutes=5),
}


# DAG definition
with DAG(
    dag_id='dag_with_minio_s3_v2',
    default_args=default_args,
    start_date=datetime(2024, 9, 28),
    schedule_interval='@daily',
) as dag:
    s3_sensor = S3KeySensor(
        task_id='s3_minio_sensor',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_conn',
        poke_interval=5,
        timeout=30,
    )