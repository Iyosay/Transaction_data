"""
Airflow DAG for Generating and Loading Skincare Transaction Data to Redshift via S3.

This DAG performs the following daily tasks:
1. Generates synthetic skincare transaction data using Faker and uploads it to S3 in Parquet format.
2. Transfers the Parquet file from S3 to a Redshift table using the S3ToRedshiftOperator.

"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import \
    S3ToRedshiftOperator

from transaction_data_s3 import skincare_transaction_data

default_args = {
    "owner": "Joy",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

# Define the DAG
dag = DAG(
    dag_id="skincare_transaction_data",
    description="This is the dag for transaction data dump to s3",
    start_date=datetime(2025, 7, 28),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
)

generate_faker_data = PythonOperator(
    task_id="generate_data", dag=dag, python_callable=skincare_transaction_data
)

file_date = datetime.today().strftime("%Y-%m-%d")
s3_path = (
    f"s3://joy-skincare-daily-transaction-data/transactions/{file_date}_tranx.parquet"
)
s3_key = f"transactions/{file_date}_tranx.parquet"

# Load Parquet data from S3 into Redshift
skincare_transaction_data_parquet_to_redshift = S3ToRedshiftOperator(
    task_id="skincare_transaction_data_parquet_to_redshift",
    schema="public",
    table="skincare_transactions",
    s3_bucket="joy-skincare-daily-transaction-data",
    s3_key=s3_key,
    copy_options=["FORMAT AS PARQUET"],
    redshift_conn_id="redshift_default",
    aws_conn_id="aws_default",
    dag=dag,
)
# task dependencies: generate -> transfer to Redshift
generate_faker_data >> skincare_transaction_data_parquet_to_redshift
