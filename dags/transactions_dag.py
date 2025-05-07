from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import timedelta
import pendulum

default_args = {
    "owner": "Hasan Çatalgöl",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="iceberg_transactions",
    description="Register Iceberg table via Hive Metastore",
    schedule=None,
    start_date=pendulum.datetime(2024, 5, 1, tz="UTC"),
    catchup=False,
    default_args=default_args,
    tags=["spark", "iceberg", "postgres", "minio", "hive"],
) as dag:

    run_transactions_job = SparkSubmitOperator(
        task_id="spark_submit_transactions",
        application="/opt/spark/scripts/load_transactions.py",
        conn_id="spark_default"
    )
