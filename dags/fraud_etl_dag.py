from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append("/usr/local/airflow")

from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data_to_postgres

import pandas as pd


RAW_FILE_PATH = "data/raw/bank_transactions.csv"
PROCESSED_FILE_PATH = "data/processed/cleaned_transactions.csv"
TABLE_NAME = "bank_transactions"


default_args = {
    "owner": "walid",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def extract_task():
    df = extract_data(RAW_FILE_PATH)
    df.to_csv(PROCESSED_FILE_PATH, index=False)
    return PROCESSED_FILE_PATH


def transform_task():
    df = pd.read_csv(PROCESSED_FILE_PATH)
    transformed_df = transform_data(df)
    transformed_df.to_csv(PROCESSED_FILE_PATH, index=False)
    return PROCESSED_FILE_PATH


def load_task():
    df = pd.read_csv(PROCESSED_FILE_PATH)
    load_data_to_postgres(df, TABLE_NAME)


with DAG(
    dag_id="bank_fraud_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for bank fraud transaction data",
    start_date=datetime(2026, 5, 21),
    schedule=None,
    catchup=False,
    tags=["etl", "fraud", "banking", "postgres"],
) as dag:

    extract = PythonOperator(
        task_id="extract_bank_transactions",
        python_callable=extract_task,
    )

    transform = PythonOperator(
        task_id="transform_bank_transactions",
        python_callable=transform_task,
    )

    load = PythonOperator(
        task_id="load_bank_transactions_to_postgres",
        python_callable=load_task,
    )

    extract >> transform >> load


# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# import sys
# import os

# # Add scripts folder to Python path
# sys.path.append("/usr/local/airflow/scripts")
# from scripts.etl_pipeline import run_etl_pipeline


# default_args = {
#     "owner": "walid",
#     "retries": 1,
#     "retry_delay": timedelta(minutes=2),
# }

# with DAG(
#     dag_id="bank_fraud_etl_pipeline",
#     default_args=default_args,
#     description="ETL pipeline for bank fraud transaction data",
#     start_date=datetime(2026, 5, 21),
#     schedule=None,
#     catchup=False,
#     tags=["etl", "fraud", "banking", "postgres"],
# ) as dag:

#     run_pipeline = PythonOperator(
#         task_id="run_bank_fraud_etl_pipeline",
#         python_callable=run_etl_pipeline,
#     )

#     run_pipeline