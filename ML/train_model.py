# train_model.py

import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import json

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve, roc_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline

from utils import preprocess_dataset


def load_data(path, sample_size=None):
    df = pd.read_csv(path)
    X, y, _, feature_names = preprocess_dataset(df, return_scaler=True)

    if sample_size:
        X = X[:sample_size]
        y = y[:sample_size]
    return X, y, _, feature_names



def get_models(pos_weight):
    return {
        "xgboost": XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
            use_label_encoder=False,
            tree_method="hist",
            scale_pos_weight=pos_weight,
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ),
        "logistic_regression": LogisticRegression(
            class_weight="balanced",
            solver="lbfgs",
            max_iter=1000,
            n_jobs=-1
        )
    }


import json  # n'oublie pas d'importer json en haut du fichier

def train_pipeline(model, X_train, y_train, X_test, y_test, name, output_dir, threshold=0.5):
    # Création du scaler (séparé pour pouvoir le sauvegarder)
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

    pipeline = ImbPipeline(steps=[
        ("smote", SMOTE(random_state=42)),
        ("classifier", model)
    ])

    print(f"🔧 Entraînement du modèle : {name}")
    pipeline.fit(X_train_scaled, y_train)

    # Sauvegarde des noms de colonnes
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{name}_features.json"), "w") as f:
        json.dump(X_train.columns.tolist(), f)

    # Sauvegarde du scaler
    joblib.dump(scaler, os.path.join(output_dir, f"{name}_scaler.pkl"))

    # Prédictions
    y_proba = pipeline.predict_proba(X_test_scaled)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    print(f"\n📊 Rapport de classification pour {name} (threshold={threshold:.2f}) :\n")
    report = classification_report(y_test, y_pred, target_names=["Non-Fraud", "Fraud"])
    print(report)

    cm = confusion_matrix(y_test, y_pred)

    # Sauvegarde du modèle et rapport
    joblib.dump(pipeline, os.path.join(output_dir, f"{name}_model.pkl"))
    with open(os.path.join(output_dir, f"{name}_report.txt"), "w") as f:
        f.write(f"Threshold: {threshold}\n\n")
        f.write(report)
        f.write("\nConfusion Matrix:\n")
        f.write(str(cm))

    # Courbes
    plot_roc(y_test, y_proba, name, output_dir)
    plot_pr(y_test, y_proba, name, output_dir)

    return roc_auc_score(y_test, y_proba)





def plot_roc(y_test, y_proba, name, output_dir):
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}", color="blue")
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve - {name}")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_dir, f"{name}_roc_curve.png"))
    plt.close()


def plot_pr(y_test, y_proba, name, output_dir):
    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color="green")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(f"Precision-Recall Curve - {name}")
    plt.grid()
    plt.savefig(os.path.join(output_dir, f"{name}_pr_curve.png"))
    plt.close()


def main():
    print("📥 Chargement des données...")
    csv_path = r"C:\Users\user\Desktop\Fraud_detection_project\data\transactions.csv"
    X, y, _, feature_names = load_data(csv_path, sample_size=1_000_000)  # récupère feature_names

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    pos_weight = np.sum(y == 0) / np.sum(y == 1)
    print(f"⚖️ Poids des classes : scale_pos_weight = {pos_weight:.2f}")

    models = get_models(pos_weight)
    output_dir = r"C:\Users\user\Desktop\Fraud_detection_project\ML\models"

    best_auc = 0
    best_model_name = ""

    for name, model in models.items():
        auc_score = train_pipeline(
            model, X_train, y_train, X_test, y_test, name, output_dir
    )

        print(f"✅ AUC pour {name} : {auc_score:.4f}")
        if auc_score > best_auc:
            best_auc = auc_score
            best_model_name = name

    print(f"\n🏆 Meilleur modèle : {best_model_name} avec AUC = {best_auc:.4f}")


if __name__ == "__main__":
    main()
