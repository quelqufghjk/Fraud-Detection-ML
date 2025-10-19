from airflow import DAG  # type: ignore
from airflow.operators.bash import BashOperator  # type: ignore
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='Producer_Consumer_startup',
    default_args=default_args,
    description='Démarrage du producer puis du consumer',
    schedule=None,
    start_date=datetime(2025, 7, 1),
    catchup=False,
    tags=['Produce', 'Consume']
) as dag:

    # Lance producer en arrière-plan (sans bloquer)
    run_producer = BashOperator(
        task_id='run_producer',
        bash_command="""
        nohup python3 /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka/producer.py > /tmp/producer.log 2>&1 &
        """
    )

    wait_5s = BashOperator(
        task_id='wait_5_seconds',
        bash_command='sleep 5'
    )

    run_consumer = BashOperator(
        task_id='run_consumer',
        bash_command='python3 /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka/consumer.py'
    )

    run_producer >> wait_5s >> run_consumer









# from airflow import DAG # type: ignore
# from airflow.operators.bash import BashOperator # type: ignore
# from datetime import datetime, timedelta

# default_args = {
#     'owner': 'airflow',
#     'retries': 1,
#     'retry_delay': timedelta(minutes=2),
# }

# with DAG(
#     dag_id='Producer_Consumer_startup',
#     default_args=default_args,
#     description='Démarrage du producer puis du consumer',
#     schedule=None,
#     start_date=datetime(2025, 7, 1),
#     catchup=False,
#     tags=['Produce', 'Consume']
# ) as dag:

#     run_producer = BashOperator(
#         task_id='run_producer',
#         bash_command='python3 /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka/producer.py'
#     )

#     wait_5s = BashOperator(
#         task_id='wait_5_seconds',
#         bash_command='sleep 5'
#     )

#     run_consumer = BashOperator(
#         task_id='run_consumer',
#         bash_command='python3 /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka/consumer.py'
#     )

#     run_producer >> wait_5s >> run_consumer
