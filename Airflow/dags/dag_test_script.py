from airflow import DAG # type: ignore
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime

with DAG(
    dag_id='dag_test_script_execution',
    description='Test de l\'exécution de scripts Python via BashOperator',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['test']
) as dag:

    test_task = BashOperator(
        task_id='run_test_script',
        bash_command='python3 /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka/test_script.py'
    )
