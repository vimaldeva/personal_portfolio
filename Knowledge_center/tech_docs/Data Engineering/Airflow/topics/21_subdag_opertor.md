## SubDagOperator

- Embeds a DAG inside another DAG as a single task
- Groups a set of tasks into one collapsible unit
- Not recommended in Airflow 2.x → Use TaskGroup instead
- Still good to know for maintaining legacy pipelines

```
from airflow.operators.subdag import SubDagOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

PARENT_DAG = "parent_dag"
CHILD_DAG  = "child_dag"

# Define the SubDAG
def create_subdag(parent_dag_id, child_dag_id, start_date, schedule_interval):
    with DAG(
        dag_id=f"{parent_dag_id}.{child_dag_id}",
        start_date=start_date,
        schedule_interval=schedule_interval
    ) as subdag:

        task_1 = PythonOperator(task_id="sub_task_1", python_callable=lambda: print("sub 1"))
        task_2 = PythonOperator(task_id="sub_task_2", python_callable=lambda: print("sub 2"))

        task_1 >> task_2

    return subdag

# Use it in Parent DAG
with DAG(
    dag_id=PARENT_DAG,
    start_date=datetime(2024,1,1),
    schedule_interval="@daily"
) as dag:

    start = EmptyOperator(task_id="start")

    subdag_task = SubDagOperator(
        task_id=CHILD_DAG,
        subdag=create_subdag(PARENT_DAG, CHILD_DAG, datetime(2024,1,1), "@daily")
    )

    end = EmptyOperator(task_id="end")

    start >> subdag_task >> end
```

Why SubDagOperator is discouraged

- Causes deadlocks in some executor setups
- Uses a separate SequentialExecutor internally
- Hard to debug
- TaskGroup does the same job better

TaskGroup - Modern Alternative

```
from airflow.utils.task_group import TaskGroup

with DAG(...) as dag:

    start = EmptyOperator(task_id="start")

    with TaskGroup("transformation_group") as tg:
        task_1 = PythonOperator(task_id="transform_1", ...)
        task_2 = PythonOperator(task_id="transform_2", ...)
        task_1 >> task_2

    end = EmptyOperator(task_id="end")

    start >> tg >> end
```

| Operator | Use it when |
| :-- | :-- |
| BranchPythonOperator | Route pipeline to specific tasks based on condition |
| ShortCircuitOperator | Stop or continue entire downstream pipeline |
| TriggerDagRunOperator | Trigger another DAG from current DAG |
| SubDagOperator | Group tasks together (use TaskGroup instead) |