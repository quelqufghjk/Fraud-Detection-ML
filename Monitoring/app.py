import streamlit as st
import pandas as pd
import pyodbc
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 🎨 Configuration du layout
st.set_page_config(page_title="RYUK - Supervision", layout="wide")
st.title("💳 RYUK - Système de Supervision des Transactions & Détection de Fraude")

# 🔌 Connexion et chargement de données depuis SQL Server
@st.cache_data(ttl=10)
def get_scored_data():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost,1433;"
            "DATABASE=FraudDetection;"
            "UID=SA;"
            "PWD=Mouhammmad@92"
        )
        query = """
            SELECT TOP 500 *
            FROM TransactionsScored
            ORDER BY id DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Erreur de connexion à SQL Server : {e}")
        return pd.DataFrame()

# 🔄 Bouton de rafraîchissement
if st.button("🔁 Rafraîchir les données"):
    st.cache_data.clear()

df = get_scored_data()
if df.empty:
    st.warning("Aucune transaction disponible.")
    st.stop()

# 🧹 Préparation des données
df['timestamp'] = pd.to_datetime(df['timestamp'])
fraudes = df[df['isFraudPred'] == 1]
non_fraudes = df[df['isFraudPred'] == 0]

# 🔍 Filtre dynamique
selected_type = st.selectbox("🔍 Sélectionner un type de transaction", options=sorted(df['type'].unique()))
filtered_df = df[df['type'] == selected_type]
filtered_fraudes = filtered_df[filtered_df['isFraudPred'] == 1]

# 🚨 Alerte visuelle en haut
if not filtered_fraudes.empty:
    st.toast(f"🚨 {len(filtered_fraudes)} fraude(s) détectée(s) pour les transactions de type {selected_type}", icon="⚠️")
else:
    st.success(f"✅ Aucune fraude détectée pour les transactions de type {selected_type}")

# 📊 Affichage des métriques
st.markdown("### 📈 Indicateurs clés")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Transactions filtrées", len(filtered_df), delta=len(filtered_df) - 100)

with col2:
    st.metric("⚠️ Fraudes détectées", len(filtered_fraudes), delta=len(filtered_fraudes) - 10)

with col3:
    avg_amt = filtered_df['amount'].mean()
    st.metric("💰 Montant moyen", f"${avg_amt:,.2f}", delta=-500)

# 📊 Graphiques comparatifs
st.markdown("### 📊 Visualisations des données")
col4, col5 = st.columns(2)

with col4:
    st.markdown("**Fraudes vs Non-Fraudes (par type)**")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=filtered_df, x='isFraudPred', palette=['#3498db', '#e74c3c'], ax=ax1)
    ax1.set_xticklabels(['Non Fraude', 'Fraude'])
    ax1.set_ylabel("Nombre")
    ax1.set_title("Répartition des fraudes")
    st.pyplot(fig1)

with col5:
    st.markdown("**Distribution des montants**")
    fig2, ax2 = plt.subplots()
    sns.histplot(filtered_df['amount'], bins=30, kde=True, color='purple', ax=ax2)
    ax2.set_title("Distribution des montants")
    ax2.set_xlabel("Montant")
    st.pyplot(fig2)

# 🚨 Tableau des alertes en bas
st.markdown("### 🚨 Détails des Transactions Frauduleuses")
if not filtered_fraudes.empty:
    st.dataframe(
        filtered_fraudes[['id', 'step', 'type', 'amount', 'probFraud', 'timestamp']],
        height=250,
        use_container_width=True
    )
else:
    st.info("Aucune fraude détectée pour ce type de transaction.")

# 📋 Données détaillées toutes transactions
st.markdown("### 📋 Données complètes (transactions filtrées)")
st.dataframe(
    filtered_df[['id', 'step', 'type', 'amount', 'isFraudPred', 'probFraud', 'timestamp']],
    height=300,
    use_container_width=True
)
