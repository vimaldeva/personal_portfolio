## PythonOperator
- Runs a Python function inside a task
- Most commonly used operator in Airflow

```
from airflow.operators.python import PythonOperator

# Basic usage
def my_function():
    print("Hello from Python")

task = PythonOperator(
    task_id="run_python",
    python_callable=my_function
)
```

Passing Arguments

```
def greet(name, age):
    print(f"Hello {name}, you are {age} years old")

task = PythonOperator(
    task_id="greet_task",
    python_callable=greet,
    op_kwargs={"name": "John", "age": 30}
)
```

Accessing execution date and context

```
def process_data(**context):
    execution_date = context['ds']
    print(f"Processing data for {execution_date}")

task = PythonOperator(
    task_id="process_task",
    python_callable=process_data,
    provide_context=True   # not needed in Airflow 2.x
)
```

Using TaskFlow API (Airflow 2.x cleaner way)

```
from airflow.decorators import task, dag
from datetime import datetime

@dag(start_date=datetime(2024,1,1), schedule_interval="@daily")
def my_dag():

    @task
    def extract():
        return {"data": "raw_data"}

    @task
    def transform(data):
        return {"data": "transformed"}

    @task
    def load(data):
        print("Loading data")

    raw = extract()
    transformed = transform(raw)
    load(transformed)

my_dag()
```




