## Tasks
A Task is the basic unit of execution in Airflow. Tasks are arranged into Dags, and then have upstream and downstream dependencies set between them in order to express the order they should run in.

There are three basic kinds of Task:

- Operators, predefined task templates that you can string together quickly to build most parts of your Dags.

- Sensors, a special subclass of Operators which are entirely about waiting for an external event to happen.

- A TaskFlow-decorated @task, which is a custom Python function packaged up as a Task.

#### Dependency
```
first_task >> second_task >> [third_task, fourth_task]
```

---
### Task Instances
An instance of a Task is a specific run of that task for a given Dag (and thus for a given data interval). They are also the representation of a Task that has state, representing what stage of the lifecycle it is in.

The possible states for a Task Instance are:

- one: The Task has not yet been queued for execution (its dependencies are not yet met)
- scheduled: The scheduler has determined the Task’s dependencies are met and it should run
- queued: The task has been assigned to an Executor and is awaiting a worker
- running: The task is running on a worker (or on a local/synchronous executor)
- success: The task finished running without errors
- restarting: The task was externally requested to restart when it was running
- failed: The task had an error during execution and failed to run
- skipped: The task was skipped due to branching, LatestOnly, or similar.
- upstream_failed: An upstream task failed and the Trigger Rule says we needed it
- up_for_retry: The task failed, but has retry attempts left and will be rescheduled.
- up_for_reschedule: The task is a Sensor that is in reschedule mode
- deferred: The task has been deferred to a trigger
- removed: The task has vanished from the Dag since the run started

Ideally, a task should flow from none, to scheduled, to queued, to running, and finally to success.


### Relationship Terminology

Firstly, it can have upstream and downstream tasks:

```
task1 >> task2 >> task3
```
When a Dag runs, it will create instances for each of these tasks that are upstream/downstream of each other, but which all have the same data interval.

There may also be instances of the same task, but for different data intervals - from other runs of the same Dag. We call these previous and next - it is a different relationship to upstream and downstream!

---
### Timeouts

If you want a task to have a maximum runtime, set its execution_timeout attribute to a datetime.timedelta value that is the maximum permissible runtime. This applies to all Airflow tasks, including sensors. execution_timeout controls the maximum time allowed for every execution. If execution_timeout is breached, the task times out and AirflowTaskTimeout is raised.

In addition, sensors have a timeout parameter. This only matters for sensors in reschedule mode. timeout controls the maximum time allowed for the sensor to succeed. If timeout is breached, AirflowSensorTimeout will be raised and the sensor fails immediately without retrying.

The following SFTPSensor example illustrates this. The sensor is in reschedule mode, meaning it is periodically executed and rescheduled until it succeeds.

- Each time the sensor pokes the SFTP server, it is allowed to take maximum 60 seconds as defined by execution_timeout.
- If it takes the sensor more than 60 seconds to poke the SFTP server, AirflowTaskTimeout will be raised. The sensor is allowed to retry when this happens. It can retry up to 2 times as defined by retries.
- From the start of the first execution, till it eventually succeeds (i.e. after the file ‘root/test’ appears), the sensor is allowed maximum 3600 seconds as defined by timeout. In other words, if the file does not appear on the SFTP server within 3600 seconds, the sensor will raise AirflowSensorTimeout. It will not retry when this error is raised.
- If the sensor fails due to other reasons such as network outages during the 3600 seconds interval, it can retry up to 2 times as defined by retries. Retrying does not reset the timeout. It will still have up to 3600 seconds in total for it to succeed.

```
sensor = SFTPSensor(
    task_id="sensor",
    path="/root/test",
    execution_timeout=timedelta(seconds=60),
    timeout=3600,
    retries=2,
    mode="reschedule",
)
```

### SLAs

The SLA feature from Airflow 2 has been removed in 3.0 and was replaced in Airflow 3.1 with Deadlines Alerts.

### Special Exceptions
If you want to control your task’s state from within custom Task/Operator code, Airflow provides two special exceptions you can raise:

- AirflowSkipException will mark the current task as skipped
- AirflowFailException will mark the current task as failed ignoring any remaining retry attempts

These can be useful if your code has extra knowledge about its environment and wants to fail/skip faster - e.g., skipping when it knows there’s no data available, or fast-failing when it detects its API key is invalid (as that will not be fixed by a retry).



### Task Instance Heartbeat Timeout


No system runs perfectly, and task instances are expected to die once in a while.


TaskInstances may get stuck in a running state despite their associated jobs being inactive (for example if the TaskInstance’s worker ran out of memory). Such tasks were formerly known as zombie tasks. Airflow will find these periodically, clean them up, and mark the TaskInstance as failed or retry it if it has available retries. The TaskInstance’s heartbeat can timeout for many reasons, including:

- The Airflow worker ran out of memory and was OOMKilled.
- The Airflow worker failed its liveness probe, so the system (for example, Kubernetes) restarted the worker.
- The system (for example, Kubernetes) scaled down and moved an Airflow worker from one node to another.
