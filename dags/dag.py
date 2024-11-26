import os
import sys
from datetime import datetime, timedelta
import requests

import extract
import transform
import load

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow_sensors.http_sensor import HttpSensor
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator

from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator


#params
default_args = {
    'owner': 'LongBui',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    'stock_data_etl',
    default_args = default_args,
    description = 'ETL ',
    description='ETL process for S&P 500 stock data',
    schedule_interval = "@daily",
)

start_task = DummyOperator(
    task_id = 'start',
    dag=dag
)

extract_sp500_task = PythonOperator(
    task_id = 'extract_sp500_task',
    python_callable = extract.fetch_sp500,
    provide_context = True,
    dag = dag,
)

cdc_sp500_task = PythonOperator(
    task_id = 'cdc_sp500_task',
    python_callable = load.cdc_sp500,
    provide_context = True,
    dag = dag,
)

load_sp500_to_s3 = S3CreateObjectOperator(
        task_id = 'upload_to_s3',
        aws_conn_id= 'AWS_CONN',
        s3_bucket='airflowoutputtos3bucket',
        s3_key='raw/sp500_companies.csv',
        data="{{ ti.xcom_pull(key='final_data') }}",
        dag=dag,
    )

extract_stock_task = PythonOperator(
    task_id = 'extract_stock_task',
    python_callable = extract.fetch_stock_data,
    provide_context = True,
    dag = dag,
)

extract_stock_task = PythonOperator(
    task_id = 'track_stock_statistics',
    python_callable = extract.track_stock_statistics,
    provide_context = True,
    dag = dag,
)

transform_stock_task = PythonOperator(
    task_id='transform_stock_task',
    python_callable= transform.call_all,
    provide_context=True,
    dag=dag,
)

load_stock_task = PythonOperator(
    task_id='load_stock_task',
    python_callable=load.insert_stock_data,
    provide_context=True,
    dag=dag,
)

extract_financial_task = PythonOperator(
    task_id='extract_financial_task',
    python_callable=load.track_stock_statistics,
    provide_context=True,
    dag=dag,
)

load_financial_task = PythonOperator(
    task_id='load_stock_task',
    python_callable=load.insert_financial_data,
    provide_context=True,
    dag=dag,
)

end_task = DummyOperator(
    task_id = 'end',
    dag=dag,
)

#pipelines
start_task >> extract_sp500_task >> cdc_sp500_task >> load_sp500_task 
load_sp500_task >> extract_stock_task >> transform_stock_task >> load_stock_task
load_stock_task >> extract_financial_task >> load_financial_task >> end_task