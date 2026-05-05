## Sensor
- A special type of Operator that waits for a condition to be true
- Keeps checking the condition at regular intervals
- Once condition is met → moves to next task
- If condition not met within timeout → task fails

```
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id="wait_for_file",
    filepath="/data/input/myfile.csv",
    poke_interval=30,   # check every 30 seconds
    timeout=3600,       # fail after 1 hour
    dag=dag
)
```

| Mode | Behavior |
| :-- | :-- |
| poke | Occupies a worker slot while waiting |
| reschedule | Releases worker slot between checks |
| deferrable | Most efficient, uses Triggerer component |

#### Common Sensors

- FileSensor → waits for a file to arrive
- HttpSensor → waits for API to return 200
- SqlSensor → waits for a row in DB table
- ExternalTaskSensor → waits for another DAG/task to complete
- S3KeySensor → waits for a file in S3