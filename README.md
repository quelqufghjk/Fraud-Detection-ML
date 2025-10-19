# 🏦 Real-Time Fraud Detection Pipeline using Kafka, Airflow & Machine Learning

> **Author:** Mouhamed SARR  
> 🎓 MSc Data Management — 2025  
> 🔗 [LinkedIn](https://www.linkedin.com/in/mouhamedsarr) • [GitHub](https://github.com/quelqufghjk)

---

## 🧠 Project Overview

This project implements an **end-to-end DataOps pipeline** for **real-time bank fraud detection**.  
It leverages **stream processing**, **machine learning**, and **workflow orchestration** to detect suspicious transactions on the fly.

The system integrates:
- **Kafka** for message streaming  
- **XGBoost** for predictive modeling  
- **SQL Server** for persistence  
- **Airflow** for orchestration  
- **Streamlit** for real-time monitoring
- **Docker** for containerization

---

## 🏗️ Global Architecture

```mermaid
flowchart LR
    A[Producer.py] -->|transactions JSON| B[(Apache Kafka)]
    B --> C[Consumer.py]
    C --> D[(SQL Server)]
    D --> E[Streamlit Dashboard]
    subgraph Airflow
        F(dag_pipeline_startup)
        G(dag_scoring)
        H(dag_backup)
    end
    F --> G --> H


Fraud_detection_project/
├── Kafka/
│   ├── producer.py
│   ├── consumer.py
│   ├── docker-compose.yml
│   └── utils.py
├── ML/
│   ├── model.pkl
│   ├── training.py
│   └── preprocessing.py
├── SQL/
│   ├── docker-compose.sql.yml
│   ├── init/
│   │   └── init.sql
│   └── export_sql_to_csv.py
├── airflow/
│   ├── dags/
│   │   ├── dag_pipeline_startup.py
│   │   ├── dag_scoring.py
│   │   └── dag_backup.py
│   ├── docker-compose.yml
│   └── logs/
└── streamlit_app/
    └── dashboard.py





