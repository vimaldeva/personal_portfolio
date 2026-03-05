from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator

with DAG("dag_bash_basic",
         start_date= datetime(2026,1,1),
         schedule= "@daily",
         catchup= False
         ) as dag :
    
    task_a = BashOperator(task_id = "bash_simple",
                          bash_command = "echo 'Hello! This is a nash program' "
                          )
