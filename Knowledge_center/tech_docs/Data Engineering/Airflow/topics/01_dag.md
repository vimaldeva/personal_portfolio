## DAG (Directed Acyclic Graph)

- A workflow in Airflow
- Simply a Python file that defines a set of tasks and their execution order
- Directed → tasks flow in one direction
- Acyclic → no loops allowed
- Stored in the dags/ folder

```
from airflow import DAG
from datetime import datetime

with DAG(
    dag_id="my_first_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    pass
```

