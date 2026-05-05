## EmptyOperator

- Does absolutely nothing
- Just a placeholder task
- Used for organizing and structuring DAGs
- DummyOperator → Airflow 1.x and 2.x
- EmptyOperator → Airflow 2.4+ (renamed, recommended)

```
from airflow.operators.empty import EmptyOperator
# or
from airflow.operators.dummy import DummyOperator
```

Use Case 1 → Start and End markers

```
start = EmptyOperator(task_id="start")
end   = EmptyOperator(task_id="end")

start >> [task_1, task_2, task_3] >> end
```

Use Case 2 → Branching join point

```
start         = EmptyOperator(task_id="start")
branch_task   = BranchPythonOperator(...)
task_a        = PythonOperator(...)
task_b        = PythonOperator(...)
join          = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")

start >> branch_task >> [task_a, task_b] >> join
```

Use Case 3 → Organize complex DAGs

```
# Group start and end points for clarity
extract_start = EmptyOperator(task_id="extract_start")
extract_end   = EmptyOperator(task_id="extract_end")

transform_start = EmptyOperator(task_id="transform_start")
transform_end   = EmptyOperator(task_id="transform_end")

extract_start >> [extract_1, extract_2] >> extract_end
extract_end >> transform_start >> [transform_1, transform_2] >> transform_end
```

| Operator | Use it when |
| :-- | :-- |
| BashOperator | Run shell commands or scripts |
| PythonOperator | Run Python functions |
| EmailOperator | Send email notifications |
| EmptyOperator | Placeholder, structure and organize DAG |

