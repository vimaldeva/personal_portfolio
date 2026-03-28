from airflow.decorators import dag
from datetime import datetime


@dag(start_date= datetime(2026,1,1),
     schedule = "@daily",
     catchup= False)
def dag_empty_decorator():
    pass

dag_empty_decorator()

