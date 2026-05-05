## XComs

XComs (short for “cross-communications”) are a mechanism that let Tasks talk to each other, as by default Tasks are entirely isolated and may be running on entirely different machines.

An XCom is identified by a key (essentially its name), as well as the task_id and dag_id it came from. They can have any serializable value (including objects that are decorated with @dataclass or @attr.define, see TaskFlow arguments:), but they are only designed for small amounts of data; do not use them to pass around large values, like dataframes.

XCom operations should be performed through the Task Context using get_current_context(). Directly updating using XCom database model is not possible.

XComs are explicitly “pushed” and “pulled” to/from their storage using the xcom_push and xcom_pull methods on Task Instances.

To push a value within a task called “task-1” that will be used by another task:

```
# pushes data in any_serializable_value into XCom with key "identifier as string"
task_instance.xcom_push(key="identifier as a string", value=any_serializable_value)
```

To pull the value that was pushed in the code above in a different task:


```
# pulls the XCom variable with key "identifier as string" that was pushed from within task-1
task_instance.xcom_pull(key="identifier as string", task_ids="task-1")
``` 

Many operators will auto-push their results into an XCom key called return_value if the do_xcom_push argument is set to True (as it is by default), and @task functions do this as well. xcom_pull defaults to using return_value as key if no key is passed to it, meaning it’s possible to write code like this:

```
# Pulls the return_value XCOM from "pushing_task"
value = task_instance.xcom_pull(task_ids='pushing_task')
```

```
# A task returning a dictionary
@task(do_xcom_push=True, multiple_outputs=True)
def push_multiple(**context):
    return {"key1": "value1", "key2": "value2"}


@task
def xcom_pull_with_multiple_outputs(**context):
    # Pulling a specific key from the multiple outputs
    key1 = context["ti"].xcom_pull(task_ids="push_multiple", key="key1")  # to pull key1
    key2 = context["ti"].xcom_pull(task_ids="push_multiple", key="key2")  # to pull key2

    # Pulling entire XCom data from push_multiple task
    data = context["ti"].xcom_pull(task_ids="push_multiple", key="return_value")

```
