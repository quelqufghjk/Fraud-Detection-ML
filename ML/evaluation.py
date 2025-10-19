








































# import pandas as pd
# import joblib
# import os
# import numpy as np
# from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve
# from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt
# from utils import prepocessing_data

# def main():
#     # 📥 Chargement des données brutes et du modèle
#     df = pd.read_csv(r"C:\Users\user\Desktop\Fraud_detection_project\data\transactions.csv")
#     model = joblib.load(r"C:\Users\user\Desktop\Fraud_detection_project\ML\model.pkl")

#     # ⚙️ Prétraitement
#     X, y, _ = prepocessing_data(df, return_scaler=True)

#     # 🎯 Split pour test
#     _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

#     # 🔍 Prédiction
#     threshold = 0.2
#     y_proba = model.predict_proba(X_test)[:, 1]
#     y_pred = (y_proba >= threshold).astype(int)

#     print(f"✅ Seuil de classification appliqué : {threshold}")

#     # 📊 Évaluation
#     report = classification_report(y_test, y_pred)
#     cm = confusion_matrix(y_test, y_pred)

#     # 📁 Sauvegarde
#     output_dir = r"C:\Users\user\Desktop\Fraud_detection_project\outputs"
#     os.makedirs(output_dir, exist_ok=True)

#     with open(os.path.join(output_dir, "evaluation_report.txt"), "w") as f:
#         f.write("Classification Report:\n")
#         f.write(report)
#         f.write("\nConfusion Matrix:\n")
#         f.write(str(cm))

#     print("✅ Rapport de classification sauvegardé.")

#     # 📈 Visualisations
#     plot_roc(y_test, y_proba, os.path.join(output_dir, "roc_curve.png"))
#     plot_precision_recall(y_test, y_proba, os.path.join(output_dir, "precision_recall.png"))

# def plot_roc(y_test, y_proba, output_path):
#     fpr, tpr, _ = roc_curve(y_test, y_proba)
#     roc_auc = auc(fpr, tpr)

#     plt.figure(figsize=(8, 6))
#     plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}", color="blue")
#     plt.plot([0, 1], [0, 1], "k--", label="Random")
#     plt.xlabel("False Positive Rate")
#     plt.ylabel("True Positive Rate")
#     plt.title("ROC Curve")
#     plt.legend()
#     plt.grid()
#     plt.savefig(output_path)
#     plt.close()
#     print(f"✅ Courbe ROC sauvegardée dans {output_path}")

# def plot_precision_recall(y_test, y_proba, output_path):
#     precision, recall, _ = precision_recall_curve(y_test, y_proba)

#     plt.figure(figsize=(8, 6))
#     plt.plot(recall, precision, color="green")
#     plt.xlabel("Recall")
#     plt.ylabel("Precision")
#     plt.title("Precision-Recall Curve")
#     plt.grid()
#     plt.savefig(output_path)
#     plt.close()
#     print(f"✅ Courbe Precision-Recall sauvegardée dans {output_path}")

# if __name__ == "__main__":
#     main()
