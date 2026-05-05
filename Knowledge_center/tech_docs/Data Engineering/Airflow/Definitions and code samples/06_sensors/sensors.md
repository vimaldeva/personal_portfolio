## Sensors
Sensors are a special type of Operator that are designed to do exactly one thing - wait for something to occur. It can be time-based, or waiting for a file, or an external event, but all they do is wait until something happens, and then succeed so their downstream tasks can run. Or, in the case when that thing does _not_ happen within the configured timeout, fails so that you can be alerted to the failure through the usual mechanisms.

Because they are primarily idle, Sensors have two different modes of running so you can be a bit more efficient about using them:

- poke (default): The Sensor takes up a worker slot for its entire runtime
- reschedule: The Sensor takes up a worker slot only when it is checking, and sleeps for a set duration between checks

The poke and reschedule modes can be configured directly when you instantiate the sensor; generally, the trade-off between them is latency. Something that is checking every second should be in poke mode, while something that is checking every minute should be in reschedule mode.

### Common parameters

- poke_interval
- timeout
- mode (poke, reschedule)
- soft_fail - If set to True, the sensor will be marked as SKIPPED instead of FAILED when the timeout is reached.
- exponential_backoff   - If enabled, the time between checks increases exponentially up to max_wait. This is useful when polling external systems with unpredictable availability.
- max_wait - Upper bound (in seconds) for the delay between checks when exponential_backoff is enabled.

```
BashSensor(
    task_id="wait_for_file",
    bash_command="test -f /data/input.csv",
    poke_interval=60,
    timeout=60 * 60,
    mode="reschedule",
)
```

### Common sensors
- FileSensor - Wait for a file to appear in a filesystem
- BashSensor - Wait for a bash command to return true
- PythonSensor - Wait for a Python callable to return true
- TimeSensor - Wait until a specified time of day
- TimeDeltaSensor - Wait for a specified time duration
- ExternalTaskSensor - Wait for a task in another DAG to complete






