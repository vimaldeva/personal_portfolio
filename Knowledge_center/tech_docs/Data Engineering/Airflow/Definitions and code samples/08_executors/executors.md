## Executor
Executors are the mechanism by which task instances get run. They have a common API and are “pluggable”, meaning you can swap executors based on your installation needs.

Executors are set by the executor option in the [core] section of the configuration file.

Built-in executors are referred to by name, for example

```
[core]
executor = KubernetesExecutor
```
Custom or third-party executors can be configured by providing the module path of the executor python class, for example:

```
[core]
executor = my.custom.executor.module.ExecutorClass
```

If you want to check which executor is currently set, you can use the airflow config get-value core executor command:

```
$ airflow config get-value core executor
LocalExecutor
```

---
### Executor Types
There is only one type of executor that runs tasks locally (inside the scheduler process) in the repo tree, but custom ones can be written to achieve similar results, and there are those that run their tasks remotely (usually via a pool of workers). Airflow comes configured with the LocalExecutor by default, which is a local executor, and the simplest option for execution. However, as the LocalExecutor runs processes in the scheduler process that can have an impact on the performance of the scheduler. You can use the LocalExecutor for small, single-machine production installations, or one of the remote executors for a multi-machine/cloud installation. 

#### Local Executors
Airflow tasks are run locally within the scheduler process.

Pros: Very easy to use, fast, very low latency, and few requirements for setup.

Cons: Limited in capabilities and shares resources with the Airflow scheduler.

#### Remote Executors
Remote executors can further be divided into two categories:

##### Queued/Batch Executors

Airflow tasks are sent to a central queue where remote workers pull tasks to execute. Often workers are persistent and run multiple tasks at once.

Pros: More robust since you’re decoupling workers from the scheduler process. Workers can be large hosts that can churn through many tasks (often in parallel) which is cost effective. Latency can be relatively low since workers can be provisioned to be running at all times to take tasks immediately from the queue.

Cons: Shared workers have the noisy neighbor problem with tasks competing for resources on the shared hosts or competing for how the environment/system is configured. They can also be expensive if your workload is not constant, you may have workers idle, overly scaled in resources, or you have to manage scaling them up and down.

Examples:

- CeleryExecutor
- BatchExecutor
- EdgeExecutor

##### Containerized Executors

Airflow tasks are executed ad hoc inside containers/pods. Each task is isolated in its own containerized environment that is deployed when the Airflow task is queued.

Pros: Each Airflow task is isolated to one container so no noisy neighbor problem. The execution environment can be customized for specific tasks (system libs, binaries, dependencies, amount of resources, etc). Cost effective as the workers are only alive for the duration of the task.

Cons: There is latency on startup since the container or pod needs to deploy before the task can begin. Can be expensive if you’re running many short/small tasks. No workers to manage however you must manage something like a Kubernetes cluster.

Examples:

- KubernetesExecutor
- EcsExecutor

To specify an executor for a task, make use of the executor parameter on Airflow Operators:

```
BashOperator(
    task_id="hello_world",
    executor="LocalExecutor",
    bash_command="echo 'hello world!'",
)
```

```
@task(executor="LocalExecutor")
def hello_world():
    print("hello world!")
```

To specify an executor for an entire Dag, make use of the existing Airflow mechanism of default arguments. All tasks in the Dag will then use the specified executor (unless explicitly overridden by a specific task):

```
def hello_world():
    print("hello world!")


def hello_world_again():
    print("hello world again!")


with DAG(
    dag_id="hello_worlds",
    default_args={"executor": "LocalExecutor"},  # Applies to all tasks in the Dag
) as dag:
    # All tasks will use the executor from default args automatically
    hw = hello_world()
    hw_again = hello_world_again()
```
