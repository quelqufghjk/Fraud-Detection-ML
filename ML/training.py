
































# import pandas as pd
# from xgboost import XGBClassifier
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.metrics import classification_report
# import joblib
# import os
# import numpy as np
# from utils import prepocessing_data

# def main():
#     print("📥 Chargement des données brutes...")
#     df = pd.read_csv(r"C:\Users\user\Desktop\Fraud_detection_project\data\transactions.csv")

#     # ⚙️ Prétraitement via la fonction utils.py
#     X, y, _ = prepocessing_data(df, return_scaler=True)

#     # ⚠️ Utilise un échantillon ou tout le dataset selon les ressources
#     use_full_data = False
#     if not use_full_data:
#         sample_size = min(1_000_000, len(X))
#         X = X[:sample_size]
#         y = y[:sample_size]

#     # 🧮 Calcul automatique du poids pour classe déséquilibrée
#     ratio = np.sum(y == 0) / np.sum(y == 1)
#     print(f"⚖️ scale_pos_weight = {ratio:.2f}")

#     # 🎯 Split stratifié
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, stratify=y, random_state=42
#     )

#     # 🔍 Recherche des meilleurs hyperparamètres
#     print("🚀 Recherche des hyperparamètres...")
#     param_grid = {
#         'n_estimators': [100, 200, 300],
#         'max_depth': [6, 7, 8],
#         'learning_rate': [0.01, 0.1, 0.2],
#         'subsample': [0.8, 1.0],
#         'colsample_bytree': [0.8, 1.0],
#         'scale_pos_weight': [ratio]
#     }

#     model = XGBClassifier(
#         objective='binary:logistic',
#         eval_metric='logloss',
#         tree_method='hist',  # rapide et efficace
#         random_state=42,
#         n_jobs=-1
#     )

#     grid_search = GridSearchCV(
#         estimator=model,
#         param_grid=param_grid,
#         scoring='f1',
#         cv=3,
#         verbose=1,
#         n_jobs=-1
#     )

#     grid_search.fit(X_train, y_train)

#     best_model = grid_search.best_estimator_
#     print(f"🔍 Meilleurs paramètres trouvés : {grid_search.best_params_}")

#     # Évaluation rapide
#     y_pred = best_model.predict(X_test)
#     print("📊 Rapport sur le jeu de test :")
#     print(classification_report(y_test, y_pred))

#     # Sauvegarde du modèle
#     model_dir = r"C:\Users\user\Desktop\Fraud_detection_project\ML"
#     os.makedirs(model_dir, exist_ok=True)

#     joblib.dump(best_model, os.path.join(model_dir, "model.pkl"))

#     print("✅ Modèle sauvegardé avec succès.")

# if __name__ == "__main__":
#     main()
