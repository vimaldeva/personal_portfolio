## Scheduler

- The brain of Airflow
- Continuously reads DAG files and monitors task states
- Decides when to trigger a DAG Run based on schedule
- Submits ready tasks to the Executor
- Updates task states in Metadata Database

```
Scheduler does this in a loop →

1. Read DAG files from dags/ folder
2. Check if any DAG Run needs to be created
3. Check task dependencies
4. Submit ready tasks to Executor
5. Update states in Metadata DB
6. Repeat

```

Key Scheduler Configs

```
# How often scheduler checks for new DAGs
min_file_process_interval = 30

# How many DAG runs can happen in parallel
max_active_runs_per_dag = 16

# How many tasks can run in parallel globally
parallelism = 32
```
How all 4 work together

```
FileSensor (Sensor)
    ↓ file arrived
PostgresHook (Hook) → connects to DB
    ↓
Scheduler → sees task is ready → sends to Executor
    ↓
Executor → assigns to Worker → task runs
```

