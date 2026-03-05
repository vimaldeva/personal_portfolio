from airflow import DAG
from datetime import datetime
from airflow.providers.smtp.operators.smtp import EmailOperator

with DAG("dag_email_sample",
         start_date= datetime(2026,1,1),
         schedule= "@daily",
         catchup= False) as dag :
    
    send_email_task = EmailOperator(task_id = "email_sender",
                                    to = "vimaldeva10@gmail.com",
                                    subject = "Airflow Alert : Testing Task",
                                    html_content = """
            <h3>Task Completed</h3>
            <p>Your Airflow DAG has finished successfully.</p> """   )
