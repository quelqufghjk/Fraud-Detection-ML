import pyodbc
import pandas as pd
from datetime import datetime
import os
import platform
# 🔧 Configuration de la connexion à SQL Server LocalDB
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=localhost,1433;"
    r"DATABASE=FraudDetection;"
    r"UID=SA;"
    r"PWD=Mouhammmad@92"
)

try:
    # 📥 Connexion et lecture des données
    conn = pyodbc.connect(conn_str)
    query = "SELECT * FROM TransactionsScored"
    df = pd.read_sql(query, conn)
    conn.close()

    # 📁 Création du dossier d’archive s’il n’existe pas
    #archive_dir = r"C:\Users\user\Desktop\Fraud_detection_project\outputs\archive"
    
    if platform.system() == "Windows":
        archive_dir = r'C:\Users\user\Desktop\Fraud_detection_project\outputs\archive'
    else:
        archive_dir = '/mnt/c/Users/user/Desktop/Fraud_detection_project/outputs/archive'


    os.makedirs(archive_dir, exist_ok=True)

    # 📦 Nom du fichier de sortie
    today_str = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(archive_dir, f"backup_{today_str}.csv")

    # 💾 Sauvegarde en CSV
    df.to_csv(file_path, index=False)
    print(f"✅ Export réussi : {file_path}")

except Exception as e:
    print(f"❌ Erreur lors de l’export : {e}")