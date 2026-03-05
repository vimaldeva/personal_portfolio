from airflow import DAG
from datetime import datetime
# from airflow.operators.python import PythonOperator
from airflow.providers.standard.operators.python import PythonOperator
import logging
from airflow.operators.bash import BashOperator


def greet_task_a(**kwargs):
    logging.info("Hello! This is task A")
    # print("Hello! This is task A")

def greet_task_b(**kwargs):
    print("Hello! This is task B")

def greet_task_c(**kwargs):
    print("Hello! This is task C")

with DAG("dag-dependency-python-simple",
        start_date= datetime(2026,1,1),
        schedule = "@daily",
        catchup= False  ) as dag :    
    task_1 = PythonOperator(task_id = "task_a",
                            python_callable= greet_task_a)

    task_2 = PythonOperator(task_id = "task_b",
                            python_callable= greet_task_b)

    task_3 = PythonOperator(task_id = "task_c",
                            python_callable= greet_task_c)
    

    task_1 >> task_2 >> task_3 
