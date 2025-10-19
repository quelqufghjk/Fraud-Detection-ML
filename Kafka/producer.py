from kafka import KafkaProducer
import pandas as pd
import json
import time
import os
import platform

TOPIC_NAME = 'transactions'
KAFKA_SERVER = 'localhost:9092'  # pour usage local

# 📂 Chemin vers le fichier CSV selon l'OS
csv_path = (
    r'C:\Users\user\Desktop\Fraud_detection_project\data\simulation_dataset1.csv'
    if platform.system() == "Windows"
    else '/mnt/c/Users/user/Desktop/Fraud_detection_project/data/simulation_dataset1.csv'
)

assert os.path.exists(csv_path), f"❌ Fichier CSV introuvable : {csv_path}"

# 📥 Chargement des données
transactions_df = pd.read_csv(csv_path)

# 🛠️ Initialisation du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print(f"✅ Producteur Kafka initialisé — {len(transactions_df)} transactions à envoyer.")

try:
    for idx, row in transactions_df.iterrows():
        transaction = row.to_dict()
        producer.send(TOPIC_NAME, transaction)
        print(f"📤 Transaction {idx + 1} envoyée: {transaction}")
        time.sleep(1)  # ⏱️ Envoi toutes les 1s (modifie si tu veux un rythme plus rapide)
except KeyboardInterrupt:
    print("⛔️ Interruption manuelle détectée.")
finally:
    producer.flush()
    producer.close()
    print("✅ Producteur arrêté proprement.")
