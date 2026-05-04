### Core Concepts
DAG (Directed Acyclic Graph)
DAG Run
Task
Task Instance
Operator
Sensor
Hook
Executor
Scheduler
Worker
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
BashOperator
PythonOperator
EmailOperator
DummyOperator / EmptyOperator
BranchPythonOperator
ShortCircuitOperator
TriggerDagRunOperator
SubDagOperator
TaskGroup
ExternalTaskSensor
HttpOperator
SqlOperator

---
### DAG Configuration
schedule_interval
start_date
end_date
catchup
max_active_runs
default_args
dag_id
tags
concurrency
retries
retry_delay
depends_on_past
SLA (Service Level Agreement)
timeout
on_failure_callback
on_success_callback
on_retry_callback

---
### Executors
SequentialExecutor
LocalExecutor
CeleryExecutor
KubernetesExecutor
CeleryKubernetesExecutor
DaskExecutor

---
### Task Dependencies
set_upstream()
set_downstream()
Bitshift Operators (>> <<)
trigger_rule
ALL_SUCCESS
ALL_FAILED
ALL_DONE
ONE_SUCCESS
ONE_FAILED
NONE_FAILED
NONE_SKIPPED

---
### Task States
Running
Success
Failed
Skipped
Upstream Failed
Queued
Scheduled
Deferred
Up for Retry
Removed
Zombie

---
### Sensors
FileSensor
HttpSensor
SqlSensor
S3KeySensor
ExternalTaskSensor
TimeSensor
DateTimeSensor
poke_interval
timeout
mode (poke / reschedule / deferrable)
soft_fail

---
### Hooks
PostgresHook
MySqlHook
S3Hook
HttpHook
SlackHook
SparkHook
BigQueryHook
RedshiftHook
HiveHook

---
### Cloud Providers & Integrations
Amazon AWS Provider
Google Cloud Provider
Microsoft Azure Provider
Apache Spark
Apache Hive
Apache Kafka
Databricks
dbt
Snowflake
BigQuery

---
### Airflow Architecture
Single Node Architecture
Multi Node Architecture
Celery Broker (Redis / RabbitMQ)
Flower UI
DAG Processor
DAG Serialization
DAG Bag

---
### Templating & Macros
Jinja Templating
execution_date
ds
ts
prev_ds
next_ds
macros.ds_add
macros.ds_format
params
render_template_as_native_obj

---
### TaskFlow API (Airflow 2.x)
@dag decorator
@task decorator
@task.branch
@task.sensor
@task.virtualenv
@task.docker
Automatic XCom passing

---
### Dynamic DAGs
DAG Factory
Dynamic Task Mapping
expand()
partial()
map()

---
### Airflow CLI
airflow dags list
airflow tasks list
airflow dags trigger
airflow dags backfill
airflow dags pause / unpause
airflow tasks test
airflow db init
airflow db upgrade
airflow users create
airflow connections add
airflow variables set

---
### Monitoring & Logging
Gantt Chart
Tree View
Graph View
Task Duration
Task Tries
Landing Times
Log File Location
Remote Logging (S3 / GCS / Azure)
StatsD
Prometheus
Grafana Integration
Elasticsearch
---
### Security
RBAC (Role Based Access Control)
Fernet Key
Webserver Authentication
LDAP Integration
OAuth
Kerberos
Secrets Backend
AWS Secrets Manager
HashiCorp Vault
environment variables

---
### Best Practices & Patterns
Idempotency
Atomicity
Backfill
Re-run
Incremental Loading
Full Refresh
ETL Pattern
ELT Pattern
Data Partitioning
Watermarking

---
### Deployment
Docker
Docker Compose
Kubernetes (K8s)
Helm Chart
MWAA (Managed Workflows for Apache Airflow)
Cloud Composer
Astronomer
Virtual Environment
requirements.txt
plugins folder
dags folder

---
### Airflow 2.x Specific
Stable REST API
Smart Sensors
Deferrable Operators
Triggerer Component
Data-aware Scheduling
Dataset
AIP-42
Dynamic Task Mapping (AIP-42)

---
### Performance Tuning
parallelism
max_active_tasks_per_dag
worker_concurrency
dag_file_processor_timeout
min_file_process_interval
max_active_runs_per_dag