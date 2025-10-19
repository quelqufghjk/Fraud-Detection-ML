from airflow import DAG # type: ignore
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='daily_backup_transactions',
    default_args=default_args,
    description='Backup quotidien des transactions scorées depuis SQL Server',
    schedule='59 23 * * *',  # Tous les jours à 23h
    start_date=datetime(2025, 7, 5),
    catchup=False,
    tags=['backup', 'sql']
) as dag:

    export_csv = BashOperator(
        task_id='export_sql_to_csv',
        bash_command='python3 /mnt/c/Users/user/Desktop/Fraud_detection_project/SQL/export_sql_to_csv.py'
    )
