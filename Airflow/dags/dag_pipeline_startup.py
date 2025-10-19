from airflow import DAG  # type: ignore
from airflow.operators.bash import BashOperator  # type: ignore
from datetime import datetime, timedelta
from airflow.operators.trigger_dagrun import TriggerDagRunOperator # type: ignore

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='fraud_detection_pipeline',
    default_args=default_args,
    description='Pipeline Kafka → ML → SQL + Backup CSV',
    schedule=None,  # manuel
    start_date=datetime(2025, 7, 1),
    catchup=False,
    tags=['fraud', 'kafka', 'ml']
) as dag:

    # check_docker = BashOperator(
    #     task_id='check_docker',
    #     bash_command="""
    #     if ! docker info > /dev/null 2>&1; then
    #         echo "❌ Docker is not running. Please start Docker Desktop manually.";
    #         exit 1
    #     else
    #         echo "✅ Docker is running.";
    #     fi
    #     """,
    # )

    start_zookeeper = BashOperator(
        task_id='start_zookeeper',
        bash_command='cd /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka && docker-compose start zookeeper'
    )

    wait_5s = BashOperator(
        task_id='wait_5_seconds',
        bash_command='sleep 5'
    )

    start_kafka = BashOperator(
        task_id='start_kafka',
        bash_command='cd /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka && docker-compose start kafka'
    )

    wait_10s = BashOperator(
        task_id='wait_10_seconds',
        bash_command='sleep 10'
    )

    start_kafka1 = BashOperator(
        task_id='start_kafka1',
        bash_command='cd /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka && docker-compose start kafka'
    )

    wait_10s_more = BashOperator(
        task_id='wait_10_seconds_more',
        bash_command='sleep 10'
    )

    start_kafka2 = BashOperator(
        task_id='start_kafka2',
        bash_command='cd /mnt/c/Users/user/Desktop/Fraud_detection_project/Kafka && docker-compose start kafka'
    )

    # check_kafka_ready = BashOperator(
    # task_id='check_kafka_ready',
    # bash_command="""
    # ATTEMPTS=0
    # MAX_ATTEMPTS=5
    # WAIT_SECONDS=10

    # while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    #     echo "🔁 Tentative $((ATTEMPTS+1)) : Vérification de Kafka..."

    #     # Vérifie si le conteneur kafka est en état 'running'
    #     if docker inspect -f '{{.State.Running}}' kafka 2>/dev/null | grep true > /dev/null; then
    #         echo "✅ Kafka est actif."
    #         exit 0
    #     else
    #         echo "⚠️ Kafka n'est pas encore prêt. Redémarrage..."
    #         docker start kafka > /dev/null 2>&1
    #         sleep $WAIT_SECONDS
    #         ATTEMPTS=$((ATTEMPTS + 1))
    #     fi
    # done

    # echo "❌ Kafka n'a pas pu démarrer après $MAX_ATTEMPTS tentatives."
    # exit 1
    # """
    # )


    create_kafka_topic = BashOperator(
    task_id='create_kafka_topic',
    bash_command=
        'docker exec kafka kafka-topics --bootstrap-server kafka:29092 --create --if-not-exists --topic transactions --partitions 3 --replication-factor 1'
    
    )

    start_sql = BashOperator(
        task_id='start_sql_server',
        bash_command='cd /mnt/c/Users/user/Desktop/Fraud_detection_project/SQL && docker-compose start'
    )

    trigger_next_dag = TriggerDagRunOperator(
        task_id="trigger_producer_consumer",
        trigger_dag_id="Producer_Consumer_startup",  # Le dag_id EXACT du second DAG
        wait_for_completion=False  # ou True si tu veux attendre sa fin (optionnel)
    )

    start_zookeeper >> wait_5s >> start_kafka >> wait_10s >> start_kafka1 >> wait_10s_more >> start_kafka2 >> create_kafka_topic >> start_sql >> trigger_next_dag
