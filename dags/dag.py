import os
import sys
from datetime import datetime, timedelta
import requests

import extract
import transform
import load

from airflow import DAG
from airflow.operators.python import PythonOperator

#params
default_args = {
    'owner': 'LongBui',
    'start_date': datetime(2024, 10, 10),
}


dag = DAG(
    'stock_data_etl',
    default_args = default_args,
    description = 'ETL ',
    description='ETL process for S&P 500 stock data',
    schedule_interval=timedelta(days=1),
)

extract_sp500_task = PythonOperator(
    task_id = 'extract_sp500_task',
    python_callable = extract.fetch_sp500,
    provide_context = True,
    dag = dag,
)

extract_stock_task = PythonOperator(
    task_id = 'extract_stock_task',
    python_callable = extract.fetch_stock_data,
    provide_context = True,
    dag = dag,
)

extract_financial_task = PythonOperator(
    task_id = 'track_stock_statistics',
    python_callable = extract.track_stock_statistics,
    provide_context = True,
    dag = dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable= transform.transform_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load.load_data,
    provide_context=True,
    dag=dag,
)

extract_sp500_task >> extract_financial_task >> extract_stock_task >> transform_task >> load_task