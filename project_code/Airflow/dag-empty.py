from airflow import DAG
from datetime import datetime

with DAG("dag-empty",
         start_date = datetime(2026,1,1),
         schedule_interval= "@daily",
         catchup= False
         ) as dag:
    pass
    
