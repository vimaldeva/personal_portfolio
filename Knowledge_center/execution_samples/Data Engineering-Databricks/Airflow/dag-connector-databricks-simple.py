from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='databricks_serverless_trigger',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule ='@daily',
    catchup=False,
    tags=['databricks', 'serverless']
) as dag:

    run_serverless_notebook = DatabricksRunNowOperator(
        task_id='trigger_serverless_job',
        
        # Connection ID configured in Airflow Admin -> Connections
        databricks_conn_id='databricks_personal',
        
        # The Job ID you created in Step 1
        job_id=938892326574988, 
        
        # Pass parameters to the notebook widgets
        # notebook_params={
        #     "process_date": "{{ ds }}",
        #     "source_table": "raw_sales_data",
        #     "mode": "overwrite"
        # }
    )

    run_serverless_notebook
