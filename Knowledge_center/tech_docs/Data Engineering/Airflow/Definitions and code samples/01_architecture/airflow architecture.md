## Airflow components
- Scheduler - A scheduler, which handles both triggering scheduled workflows, and submitting Tasks to the executor to run. The executor, is a configuration property of the scheduler, not a separate component and runs within the scheduler process. There are several executors available out of the box, and you can also write your own.
- A Dag processor, which parses Dag files and serializes them into the metadata database. More about processing Dag files can be found in Dag File Processing
- A webserver, which presents a handy user interface to inspect, trigger and debug the behaviour of Dags and tasks.
- A folder of Dag files, which is read by the scheduler to figure out what tasks to run and when to run them.
- A metadata database, usually PostgreSQL or MySQL, which stores the state of tasks, Dags and variables.

#### Optional components
- Optional worker, which executes the tasks given to it by the scheduler. In the basic installation worker might be part of the scheduler not a separate component. It can be run as a long running process in the CeleryExecutor, or as a POD in the KubernetesExecutor.
- Optional triggerer, which executes deferred tasks in an asyncio event loop. In basic installation where deferred tasks are not used, a triggerer is not necessary. More about deferring tasks can be found in Deferrable Operators & Triggers.
- Optional folder of plugins. Plugins are a way to extend Airflow’s functionality (similar to installed packages). Plugins are read by the scheduler, Dag processor, triggerer and webserver. More about plugins can be found in Plugins.

---
### Workloads
A Dag runs through a series of Tasks, and there are three common types of task you will see:

- Operators, predefined tasks that you can string together quickly to build most parts of your Dags.
- Sensors, a special subclass of Operators which are entirely about waiting for an external event to happen.
- A TaskFlow-decorated @task, which is a custom Python function packaged up as a Task.

Internally, these are all actually subclasses of Airflow’s BaseOperator, and the concepts of Task and Operator are somewhat interchangeable, but it’s useful to think of them as separate concepts - essentially, Operators and Sensors are templates, and when you call one in a Dag file, you’re making a Task.

### Control Flow

Tasks have dependencies declared on each other. You’ll see this in a Dag either using the >> and << operators:

```
first_task >> [second_task, third_task]
fourth_task << third_task
```

To pass data between tasks you have three options:

- XComs (“Cross-communications”), a system where you can have tasks push and pull small bits of metadata.
- Uploading and downloading large files from a storage service (either one you run, or part of a public cloud)
- TaskFlow API automatically passes data between tasks via implicit XComs