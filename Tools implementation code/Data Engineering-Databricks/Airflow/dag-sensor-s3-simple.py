from airflow import DAG
from datetime import datetime
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python import PythonOperator

def file_found_callback(**kwargs):
    print("File found! Starting processing...")

with DAG("dag_s3_sensor",
         start_date= datetime(2026,1,1),
         schedule= "@daily",
         catchup= False) as dag :
    
    wait_for_s3_file = S3KeySensor(task_id = "s3_sensor",
                                   bucket_name = "vimal-practise",
                                   bucket_key = 'airflow_test/test.txt',
                                   aws_conn_id = "aws_default",
                                   mode = "reschedule",
                                   poke_interval = 30,
                                   timeout = 60*60*2
                                
                                   )
    
    process_file = PythonOperator(
        task_id='process_file',
        python_callable=file_found_callback
    )    
    wait_for_s3_file >> process_file
