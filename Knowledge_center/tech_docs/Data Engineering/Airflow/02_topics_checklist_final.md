### Core Concepts
DAG (Directed Acyclic Graph)
Task
Operator
Sensor
Hook
Executor ( also in AWS MVAA)
Scheduler 
Worker ( also in AWS MVAA)
Webserver
Metadata Database
XCom
Variable
Connection
Pool
Queue
Trigger
TaskFlow API

---
### Operators
- BashOperator , PythonOperator,EmailOperator,EmptyOperator,BranchPythonOperator,ShortCircuitOperator,TriggerDagRunOperator,SubDagOperator,TaskGroup,ExternalTaskSensor,HttpOperator,SqlOperator

### DAG Configuration

---
### Executors
SequentialExecutor,LocalExecutor,CeleryExecutor,KubernetesExecutor,CeleryKubernetesExecutor,DaskExecutor

----

- Branching strategy
- Dependency Trigger rule
- Depend on another dag (External DAG sensor)
- Trigger another dag (TriggerDagRunOperator)
- Deadline Alerts
- Dynamic DAGS
- Architecture and Components
- Macros
- Jinja Templating
- TaskFlow API
