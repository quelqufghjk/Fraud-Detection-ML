import os
import platform
import joblib
import numpy as np
import sys

# 🔧 Ajouter le chemin vers utils si besoin
UTILS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ML'))
if UTILS_PATH not in sys.path:
    sys.path.append(UTILS_PATH)

from utils import preprocess_transaction

# 📦 Chemin dynamique du modèle selon l'OS
if platform.system() == "Windows":
    model_path = r'C:\Users\user\Desktop\Fraud_detection_project\ML\models\xgboost_model.pkl'
else:
    model_path = '/mnt/c/Users/user/Desktop/Fraud_detection_project/ML/models/xgboost_model.pkl'

# ✅ Chargement du modèle
try:
    model = joblib.load(model_path)
except Exception as e:
    raise RuntimeError(f"❌ Erreur lors du chargement du modèle : {e}")

# ⚠️ Tentative de récupération des noms de colonnes attendues
try:
    expected_columns = model.feature_names_in_.tolist()
except AttributeError:
    # Si ce n'est pas un modèle sklearn classique (ex: pipeline), tenter de charger depuis le .json
    try:
        import json
        feature_path = model_path.replace("_model.pkl", "_features.json")
        with open(feature_path, "r") as f:
            expected_columns = json.load(f)
    except Exception as e:
        raise RuntimeError(f"❌ Impossible de récupérer les colonnes attendues : {e}")


# 🔍 Fonction principale de prédiction
def predict_fraud(tx_dict):
    """
    Prédit si une transaction est frauduleuse.

    Args:
        tx_dict (dict): Une transaction unique au format JSON/dict.

    Returns:
        tuple: (is_fraud (int), prob_fraud (float))
    """
    try:
        X = preprocess_transaction(tx_dict, expected_columns=expected_columns)

        if X is None or X.empty:
            raise ValueError("🚫 Transaction transformée vide ou invalide.")

        # Vérification de dimensions correctes
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X)[0][1]
        else:
            y_proba = 0.0  # fallback
        y_pred = model.predict(X)[0]

        return int(y_pred), float(y_proba)

    except Exception as e:
        print(f"❌ Erreur lors du traitement de la transaction : {e}")
        raise  # Laisse remonter l'erreur pour affichage côté consumer
