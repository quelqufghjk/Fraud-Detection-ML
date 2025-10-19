# # utils.py

# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# from typing import Tuple, Optional


# # 🚀 Transformation commune pour toutes les transactions
# def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()

#     # Encodage des types de transaction
#     df = pd.get_dummies(df, columns=["type"], drop_first=True)

#     # Forcer la présence de toutes les colonnes dummies
#     for col in ['type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT', 'type_TRANSFER']:
#         if col not in df.columns:
#             df[col] = 0

#     # Variables d'identité
#     df["dest"] = df["nameDest"].str.startswith("M").astype(int)
#     df["orig"] = df["nameOrig"].str.startswith("M").astype(int)

#     # Features supplémentaires
#     df["log_amount"] = np.log1p(df["amount"])
#     df["amount_vs_balance_orig"] = df["amount"] / (df["oldbalanceOrg"] + 1)
#     df["amount_vs_balance_dest"] = df["amount"] / (df["oldbalanceDest"] + 1)
#     df["orig_balance_change"] = df["newbalanceOrig"] - df["oldbalanceOrg"]
#     df["dest_balance_change"] = df["newbalanceDest"] - df["oldbalanceDest"]
#     df["flag_neg_newbalanceOrig"] = (df["newbalanceOrig"] < 0).astype(int)
#     df["flag_orig_no_balance"] = ((df["oldbalanceOrg"] == 0) & (df["amount"] > 0)).astype(int)
#     df["flag_dest_no_balance"] = ((df["oldbalanceDest"] == 0) & (df["amount"] > 0)).astype(int)

#     # Nettoyage
#     df.drop(["nameOrig", "nameDest"], axis=1, errors='ignore', inplace=True)

#     return df


# def preprocess_dataset(
#     df: pd.DataFrame, return_scaler: bool = False
# ) -> Tuple[np.ndarray, pd.Series, Optional[StandardScaler], list]:
#     df_fe = feature_engineering(df)

#     y = df_fe["isFraud"]
#     X = df_fe.drop(columns=["isFraud"], errors='ignore')

#     feature_names = X.columns.tolist()  # <-- récupère les noms des colonnes

#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)

#     if return_scaler:
#         return X_scaled, y, scaler, feature_names
#     else:
#         return X_scaled, y, None, feature_names



# # 📩 Pour une seule transaction Kafka (dict)
# def preprocess_transaction(
#     tx_dict: dict, expected_columns: Optional[list] = None
# ) -> pd.DataFrame:
#     df = pd.DataFrame([tx_dict])
#     df_fe = feature_engineering(df)

#     # Assurer l'ordre des colonnes
#     if expected_columns:
#         df_fe = df_fe.reindex(columns=expected_columns, fill_value=0)

#     return df_fe


































# # import pandas as pd
# # import numpy as np
# # from sklearn.preprocessing import StandardScaler

# # def prepocessing_data(df, return_scaler=False):
# #     """
# #     Prétraitement pour l'entraînement ou l'évaluation.
# #     Applique transformations + normalisation + feature engineering.
# #     """
# #     df = df.copy()

# #     df = pd.get_dummies(df, columns=['type'], drop_first=True)

# #     for col in ['type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT', 'type_TRANSFER']:
# #         if col not in df:
# #             df[col] = 0

# #     df['dest'] = df['nameDest'].str.startswith('M').astype(int)
# #     df['orig'] = df['nameOrig'].str.startswith('M').astype(int)

# #     df['log_amount'] = np.log1p(df['amount'])
# #     df['amount_vs_balance_orig'] = df['amount'] / (df['oldbalanceOrg'] + 1)
# #     df['amount_vs_balance_dest'] = df['amount'] / (df['oldbalanceDest'] + 1)
# #     df['orig_balance_change'] = df['newbalanceOrig'] - df['oldbalanceOrg']
# #     df['dest_balance_change'] = df['newbalanceDest'] - df['oldbalanceDest']
# #     df['flag_neg_newbalanceOrig'] = (df['newbalanceOrig'] < 0).astype(int)
# #     df['flag_orig_no_balance'] = ((df['oldbalanceOrg'] == 0) & (df['amount'] > 0)).astype(int)
# #     df['flag_dest_no_balance'] = ((df['oldbalanceDest'] == 0) & (df['amount'] > 0)).astype(int)

# #     df.drop(['nameOrig', 'nameDest'], axis=1, inplace=True)

# #     y = df['isFraud']
# #     X = df.drop(['isFraud'], axis=1, errors='ignore') #isflaggedFraud

# #     scaler = StandardScaler()
# #     X_scaled = scaler.fit_transform(X)

# #     if return_scaler:
# #         return X_scaled, y, scaler
# #     else:
# #         return X_scaled, y



# # def preprocessing_transaction(tx_dict, expected_columns=None):
# #     """
# #     Prétraitement d'une transaction unique reçue depuis Kafka.
# #     Reproduit les mêmes étapes que l'entraînement (sans scaling).
# #     """

# #     df = pd.DataFrame([tx_dict])

# #     df = pd.get_dummies(df, columns=["type"], drop_first=True)

# #     for col in ['type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT', 'type_TRANSFER']:
# #         if col not in df:
# #             df[col] = 0

# #     df["dest"] = df["nameDest"].str.startswith("M").astype(int)
# #     df["orig"] = df["nameOrig"].str.startswith("M").astype(int)

# #     df["log_amount"] = np.log1p(df["amount"])
# #     df["amount_vs_balance_orig"] = df["amount"] / (df["oldbalanceOrg"] + 1)
# #     df["amount_vs_balance_dest"] = df["amount"] / (df["oldbalanceDest"] + 1)
# #     df["orig_balance_change"] = df["newbalanceOrig"] - df["oldbalanceOrg"]
# #     df["dest_balance_change"] = df["newbalanceDest"] - df["oldbalanceDest"]
# #     df["flag_neg_newbalanceOrig"] = (df["newbalanceOrig"] < 0).astype(int)
# #     df["flag_orig_no_balance"] = ((df["oldbalanceOrg"] == 0) & (df["amount"] > 0)).astype(int)
# #     df["flag_dest_no_balance"] = ((df["oldbalanceDest"] == 0) & (df["amount"] > 0)).astype(int)

# #     df.drop(["nameOrig", "nameDest", "isFraud"], axis=1, errors='ignore', inplace=True)

# #     # Colonnes par défaut si le modèle ne fournit pas feature_names_in_
# #     fallback_columns = ['step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest',
# #        'newbalanceDest', 'type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT',
# #        'type_TRANSFER', 'dest', 'orig', 'log_amount',
# #        'amount_vs_balance_orig', 'amount_vs_balance_dest',
# #        'orig_balance_change', 'dest_balance_change',
# #        'flag_neg_newbalanceOrig', 'flag_orig_no_balance', 'flag_dest_no_balance','dummy']

# #     df = df.reindex(columns=expected_columns or fallback_columns, fill_value=0)
# #     return df


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional


# 🚀 Transformation commune pour toutes les transactions
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Encodage des types de transaction
    df = pd.get_dummies(df, columns=["type"], drop_first=True)

    # Forcer la présence de toutes les colonnes dummies
    for col in ['type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT', 'type_TRANSFER']:
        if col not in df.columns:
            df[col] = 0

    # Variables d'identité
    df["dest"] = df["nameDest"].str.startswith("M").astype(int)
    df["orig"] = df["nameOrig"].str.startswith("M").astype(int)

    # Features supplémentaires
    df["log_amount"] = np.log1p(df["amount"])
    df["amount_vs_balance_orig"] = df["amount"] / (df["oldbalanceOrg"] + 1)
    df["amount_vs_balance_dest"] = df["amount"] / (df["oldbalanceDest"] + 1)
    df["orig_balance_change"] = df["newbalanceOrig"] - df["oldbalanceOrg"]
    df["dest_balance_change"] = df["newbalanceDest"] - df["oldbalanceDest"]
    df["flag_neg_newbalanceOrig"] = (df["newbalanceOrig"] < 0).astype(int)
    df["flag_orig_no_balance"] = ((df["oldbalanceOrg"] == 0) & (df["amount"] > 0)).astype(int)
    df["flag_dest_no_balance"] = ((df["oldbalanceDest"] == 0) & (df["amount"] > 0)).astype(int)

    # Nettoyage
    df.drop(["nameOrig", "nameDest"], axis=1, errors='ignore', inplace=True)

    return df


def preprocess_dataset(
    df: pd.DataFrame, return_scaler: bool = False
) -> Tuple[pd.DataFrame, pd.Series, Optional[StandardScaler], list]:
    df_fe = feature_engineering(df)

    y = df_fe["isFraud"]
    X = df_fe.drop(columns=["isFraud"], errors='ignore')

    feature_names = X.columns.tolist()

    scaler = None  # On ne scale plus ici (le pipeline s'en occupe)

    if return_scaler:
        return X, y, scaler, feature_names
    else:
        return X, y, None, feature_names


# 📩 Pour une seule transaction Kafka (dict)
def preprocess_transaction(
    tx_dict: dict, expected_columns: Optional[list] = None
) -> pd.DataFrame:
    df = pd.DataFrame([tx_dict])
    df_fe = feature_engineering(df)

    # Assurer l'ordre des colonnes
    if expected_columns:
        df_fe = df_fe.reindex(columns=expected_columns, fill_value=0)

    return df_fe