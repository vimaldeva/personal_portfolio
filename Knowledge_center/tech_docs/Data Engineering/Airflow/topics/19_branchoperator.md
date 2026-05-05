## BranchPythonOperator
- Runs a Python function that returns a task_id
- Airflow executes that returned task and skips all others
- Used when you need conditional branching in your pipeline

```
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

def decide_branch():
    day = datetime.now().weekday()
    if day == 0:  # Monday
        return "monday_task"
    else:
        return "other_day_task"

branch = BranchPythonOperator(
    task_id="branch_task",
    python_callable=decide_branch
)

monday_task    = EmptyOperator(task_id="monday_task")
other_day_task = EmptyOperator(task_id="other_day_task")

branch >> [monday_task, other_day_task]
```

Branch based on row count

```
def check_data(**context):
    row_count = get_row_count()  # some function
    if row_count > 1000:
        return "process_large_data"
    elif row_count > 0:
        return "process_small_data"
    else:
        return "send_empty_alert"

branch = BranchPythonOperator(
    task_id="check_data_branch",
    python_callable=check_data
)
```
Branching with a join at the end

```
def my_branch():
    return "task_a"  # skips task_b

branch   = BranchPythonOperator(task_id="branch", python_callable=my_branch)
task_a   = EmptyOperator(task_id="task_a")
task_b   = EmptyOperator(task_id="task_b")

# trigger_rule needed so join runs even when task_b is skipped
join     = EmptyOperator(
                task_id="join",
                trigger_rule="none_failed_min_one_success"
           )

branch >> [task_a, task_b] >> join
```

Return multiple branches

```
def my_branch():
    return ["task_a", "task_b"]  # runs both, skips task_c

branch >> [task_a, task_b, task_c]
```