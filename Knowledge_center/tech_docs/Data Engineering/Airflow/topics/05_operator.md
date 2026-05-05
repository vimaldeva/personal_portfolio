## Operator
- A template that defines what a task does
- When you use an Operator inside a DAG → it becomes a Task
- Airflow provides many built-in Operators

| Operator | What it does |
| :-- | :-- |
| PythonOperator | Runs a Python function |
| BashOperator | Runs a Bash command |
| EmailOperator | Sends an email |
| SqlOperator | Runs a SQL query |

```
from airflow.operators.python import PythonOperator

def my_function():
    print("Hello Airflow")

my_task = PythonOperator(
    task_id="my_task",
    python_callable=my_function,
    dag=dag
)
```
