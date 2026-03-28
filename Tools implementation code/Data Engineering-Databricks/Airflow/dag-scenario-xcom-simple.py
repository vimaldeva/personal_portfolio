from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# ---------------------------------------------------------
# 1. SENDER FUNCTION
# ---------------------------------------------------------
def push_data_function(**kwargs):
    """
    This function pushes data to XCom in two ways.
    """
    # 'ti' stands for Task Instance. It is available in kwargs.
    ti = kwargs['ti']

    # Method A: Explicit Push (You define the key)
    # Useful for sending multiple variables
    ti.xcom_push(key='model_accuracy', value=0.98)
    ti.xcom_push(key='s3_path', value='s3://my-bucket/data.csv')

    print("Data pushed explicitly.")

    # Method B: Implicit Push (Return value)
    # This automatically pushes to XCom with key='return_value'
    return "This is the return value"

# ---------------------------------------------------------
# 2. RECEIVER FUNCTION
# ---------------------------------------------------------
def pull_data_function(**kwargs):
    """
    This function pulls data from the previous task.
    """
    ti = kwargs['ti']

    # Pull Method A: Pull specific keys
    accuracy = ti.xcom_pull(task_ids='sender_task', key='model_accuracy')
    path = ti.xcom_pull(task_ids='sender_task', key='s3_path')

    # Pull Method B: Pull the return value
    # If key is not specified, it defaults to 'return_value'
    ret_val = ti.xcom_pull(task_ids='sender_task')

    print(f"Received Accuracy: {accuracy}")
    print(f"Received Path: {path}")
    print(f"Received Return Value: {ret_val}")

# ---------------------------------------------------------
# DAG DEFINITION
# ---------------------------------------------------------
with DAG(
    dag_id="xcom_classic_no_decorators",
    start_date=datetime(2024, 1, 1),
    schedule ="@daily",
    catchup=False
) as dag:

    # Task 1: Pushes data
    task_1 = PythonOperator(
        task_id='sender_task',
        python_callable=push_data_function,
        # provide_context=True is default in Airflow 2.0+, 
        # but required in older versions to access **kwargs
    )

    # Task 2: Pulls data using Python
    task_2 = PythonOperator(
        task_id='receiver_task_python',
        python_callable=pull_data_function
    )

    # Task 3: Pulls data using Bash (Jinja Templating)
    # Note: In Bash, we use {{ }} syntax. We don't need a python function.
    task_3 = BashOperator(
        task_id='receiver_task_bash',
        bash_command="echo 'The model accuracy was: {{ ti.xcom_pull(task_ids='sender_task', key='model_accuracy') }}'"
    )

    # Set Dependencies
    task_1 >> [task_2, task_3]
