from kafka import KafkaConsumer
import json
import joblib
import pyodbc
from datetime import datetime
import os
import sys
import time

# 🔁 Durée max d'exécution (3h)
MAX_DURATION = 10800
start_time = time.time()

# 🔧 Ajout du chemin vers ml_predictor
UTILS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ML'))
if UTILS_PATH not in sys.path:
    sys.path.append(UTILS_PATH)

from ml_predictor import predict_fraud

# 🛠️ Config Kafka
TOPIC_NAME = 'transactions'
KAFKA_BOOTSTRAP_SERVER = 'localhost:9092'

# 🛢️ Connexion à SQL Server (en local via Docker)
conn = pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=localhost,1433;"
    r"DATABASE=FraudDetection;"
    r"UID=SA;"
    r"PWD=Mouhammmad@92"
)
cursor = conn.cursor()

# 🔁 Consommateur Kafka
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    #auto_offset_reset='earliest',
    auto_offset_reset='latest', # commence au dernier message produit et 
                                    #ne score pas en rafale ce qui se trouve dans la file d'attente
    enable_auto_commit=False, # ← ne mémorise pas les offsets
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("✅ Consumer Kafka en écoute...")

if __name__ == "__main__":
    for message in consumer:
        if time.time() - start_time > MAX_DURATION:
            print("🕒 Temps limite atteint — fermeture du consumer.")
            break

        try:
            tx = message.value
            is_fraud, prob_fraud = predict_fraud(tx)

            print(f"📩 Transaction reçue — Probabilité : {prob_fraud:.4f} → {'🚨 FRAUDE' if is_fraud else '✅ OK'}")

            # 📥 Insertion dans SQL Server
            insert_query = """
            INSERT INTO TransactionsScored (
                step, type, amount, oldbalanceOrg, newbalanceOrig,
                oldbalanceDest, newbalanceDest, isFraudPred, probFraud, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (
                tx.get("step"),
                tx.get("type"),
                tx.get("amount"),
                tx.get("oldbalanceOrg"),
                tx.get("newbalanceOrig"),
                tx.get("oldbalanceDest"),
                tx.get("newbalanceDest"),
                is_fraud,
                prob_fraud,
                datetime.now()
            ))
            conn.commit()

        except Exception as e:
            print(f"❌ Erreur lors du traitement de la transaction : {e}")
            continue




















# from kafka import KafkaConsumer
# import json
# import joblib
# import pyodbc
# from datetime import datetime
# import os
# import sys
# import time
# import platform

# MAX_DURATION = 10800  # ~27h

# start_time = time.time()

# # 🔧 Ajouter le dossier utils au PYTHONPATH
# UTILS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ML'))
# if UTILS_PATH not in sys.path:
#     sys.path.append(UTILS_PATH)

# from utils import preprocessing_transaction

# # ⚙️ Configuration
# TOPIC_NAME = 'transactions'
# KAFKA_BOOTSTRAP_SERVER = 'localhost:9092'

# # 🧠 Charger le modèle ML

# if platform.system() == "Windows":
#     model_path = r'C:\Users\user\Desktop\Fraud_detection_project\ML\model.pkl'
# else:
#     model_path = '/mnt/c/Users/user/Desktop/Fraud_detection_project/ML/model.pkl'


# model = joblib.load(model_path)

# # 🗃️ Connexion à SQL Server (Docker -> accès local via localhost)
# conn = pyodbc.connect(
#     r"DRIVER={ODBC Driver 17 for SQL Server};"
#     r"SERVER=localhost,1433;"
#     r"DATABASE=FraudDetection;"
#     r"UID=SA;"
#     r"PWD=Mouhammmad@92"
# )
# cursor = conn.cursor()

# # 🔁 Kafka Consumer
# consumer = KafkaConsumer(
#     TOPIC_NAME,
#     bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
#     auto_offset_reset='earliest',
#     enable_auto_commit=True,
#     value_deserializer=lambda m: json.loads(m.decode('utf-8'))
# )

# print("✅ Consumer prêt. En attente de messages Kafka...")

# if __name__ == "__main__":
#     for message in consumer:
#         try:

#             if time.time() - start_time > MAX_DURATION:
#                  print("⏹️ Temps maximum atteint (10800s). Fermeture du consumer.")
#                  break
#             tx = message.value
#             X = preprocessing_transaction(tx) 

#             is_fraud = int(model.predict(X)[0])
#             prob_fraud = float(model.predict_proba(X)[0][1])

#             print(f"📩 Transaction reçue — Probabilité : {prob_fraud:.4f} → {'FRAUDE' if is_fraud else 'OK'}")

#             # 📝 Insertion dans SQL Server
#             insert_query = """
#             INSERT INTO TransactionsScored (
#                 step, type, amount, oldbalanceOrg, newbalanceOrig,
#                 oldbalanceDest, newbalanceDest, isFraudPred, probFraud, timestamp
#             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """
#             cursor.execute(insert_query, (
#                 tx.get("step"),
#                 tx.get("type"),
#                 tx.get("amount"),
#                 tx.get("oldbalanceOrg"),
#                 tx.get("newbalanceOrig"),
#                 tx.get("oldbalanceDest"),
#                 tx.get("newbalanceDest"),
#                 is_fraud,
#                 prob_fraud,
#                 datetime.now()
#             ))
#             conn.commit()

#         except Exception as e:
#             print(f"❌ Erreur lors du traitement : {e}")
#             continue
