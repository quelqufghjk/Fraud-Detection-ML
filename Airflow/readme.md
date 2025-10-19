✅ 1. dag_pipeline_startup.py

Objectif : Démarrer Kafka + Zookeeper, créer le topic transactions et lancer le producteur

Tâches :

start_kafka_stack : Lancer Kafka via Docker Compose

create_kafka_topic : Créer le topic (si non existant)

run_producer_script : Lancer producer.py

Fréquence : Manuelle (au lancement du pipeline)

✅ 2. dag_scoring.py

Objectif : Démarrer le consumer pour scorer en temps réel les transactions

Tâches :

run_consumer_script : Exécuter consumer.py (Kafka → ML → SQL Server)

Fréquence : Toutes les 5 minutes (*/5 * * * *)

✅ 3. dag_training.py

Objectif : Réentraîner le modèle avec les données les plus récentes

Tâches :

run_training_script : Lancer training.py sur augmented_data.parquet

Fréquence : Hebdomadaire ou manuelle (schedule_interval=None)

✅ 4. dag_backup.py

Objectif : Sauvegarder les prédictions depuis SQL Server vers un fichier CSV/Parquet

Tâches :

export_sql_results : Lire la table TransactionsScored

save_to_csv : Écrire dans /outputs/archive/yyyy-mm-dd.csv

Fréquence : Tous les jours à 23h (0 23 * * *)

✅ 5. dag_data_cleaning.py (optionnel)

Objectif : Supprimer les lignes obsolètes dans la base SQL Server (vieilles transactions)

Tâches :

purge_old_records : Supprimer ou archiver les lignes > 30 jours

Fréquence : Mensuelle ou hebdomadaire

✅ Tips de mise en production

Tous les scripts doivent être dans /opt/airflow/dags/scripts/

Utiliser BashOperator pour exécuter les scripts Python ou shell

Toujours activer les logs et monitoring

Stocker les fichiers exportés dans un dossier /archive/


### 🔄 Ordre d’exécution recommandé

1. `dag_pipeline_startup` : Démarre les services et envoie les transactions  
2. `dag_scoring` : Scoring continu des transactions dans Kafka  
3. `dag_backup` : Sauvegarde des prédictions scorées (quotidien à 23h)
