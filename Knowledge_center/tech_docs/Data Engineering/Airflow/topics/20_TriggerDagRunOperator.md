## TriggerDagRunOperator

- Triggers another DAG from within a DAG
- Used to chain DAGs together
- Can pass configuration to the triggered DAG
- Can wait for the triggered DAG to complete or just fire and forget

```
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

# Basic - just trigger another DAG
trigger = TriggerDagRunOperator(
    task_id="trigger_next_dag",
    trigger_dag_id="my_downstream_dag"
)
```

Trigger and wait for completion

```
trigger = TriggerDagRunOperator(
    task_id="trigger_and_wait",
    trigger_dag_id="my_downstream_dag",
    wait_for_completion=True,    # waits until triggered DAG finishes
    poke_interval=30             # checks every 30 seconds
)
```

Pass config to triggered DAG

```
trigger = TriggerDagRunOperator(
    task_id="trigger_with_config",
    trigger_dag_id="my_downstream_dag",
    conf={"date": "2024-01-01", "env": "production"},
    wait_for_completion=True
)

# In the triggered DAG - read the config
def read_config(**context):
    conf = context["dag_run"].conf
    date = conf.get("date")
    env  = conf.get("env")
    print(f"Processing {date} in {env}")
```

Common Pipeline Pattern

```
DAG 1 (Extract)
    └── TriggerDagRunOperator
            ↓
        DAG 2 (Transform)
            └── TriggerDagRunOperator
                    ↓
                DAG 3 (Load)
```

