# 📊 Dossier ML – Entraînement & Évaluation

Ce dossier contient les scripts pour entraîner un modèle de détection de fraude :

- `training.py` : Entraîne un modèle XGBoost et le sauvegarde.
- `evaluation.py` : Génère les métriques de performance.
- `utils.py` : Prétraitement des données (normalisation, séparation).

Le modèle est utilisé par `kafka/consumer.py` pour scorer en temps réel.
