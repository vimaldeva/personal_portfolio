### DAG Creation & Basics
Create a DAG that runs every day at 6 AM and executes a Python function
Create a DAG with 5 tasks that run sequentially one after another
Create a DAG with parallel tasks where task E runs only after task C and D complete
Create a DAG that runs only on weekdays
Create a DAG with a start date in the past and disable catchup
Create a DAG that automatically retries 3 times with 5 minute delay on failure
Create a DAG that sends an email when any task fails
Create a DAG that runs every 15 minutes between 8 AM and 6 PM

---
### Task Dependencies
Create a diamond shaped DAG (A → B, A → C, B → D, C → D)
Create a DAG where task D runs even if task B or C fails
Create a DAG where downstream task runs only if at least one upstream task succeeds
Create a DAG where a task runs only if all upstream tasks are done regardless of success or failure
Create a fan-out and fan-in pattern with 10 parallel tasks
Create a task that skips all downstream tasks if a condition is not met

---
### BranchPythonOperator
Create a DAG that checks if today is Monday and branches to different tasks based on the day
Create a DAG that reads a value from a database and branches to ETL or ELT pipeline based on row count
Create a DAG where branching happens based on an API response
Create a DAG with branching and make sure the join task at the end always runs
Create a multi-level branching DAG with more than 2 branches

---
### XCom
Create a DAG where task A generates a value and task B uses that value
Create a DAG where multiple tasks push values to XCom and a final task pulls all of them
Create a DAG using TaskFlow API where return values automatically pass between tasks
Create a DAG that passes a large list between tasks using XCom
Debug a DAG where XCom values are not being passed correctly between tasks

--- 
### Sensors
Create a DAG that waits for a file to arrive in a specific folder before processing
Create a DAG that waits for an API endpoint to return status 200
Create a DAG that waits for a row to appear in a database table
Create a DAG that waits for another DAG to complete successfully before starting
Create a sensor with reschedule mode instead of poke mode and explain when to use each
Create a DAG that times out after 2 hours if the sensor condition is not met
Create a deferrable sensor for an S3 file arrival

---
### Variables & Connections
Create a DAG that reads database credentials from Airflow Connections instead of hardcoding
Create a DAG that uses Airflow Variables to control environment (dev/staging/prod)
Create a DAG that reads a JSON variable and uses different keys for different tasks
Store and retrieve a secret using environment variable based connection
Create a DAG that dynamically changes behavior based on a variable flag

---
### Hooks
Create a DAG that uses PostgresHook to query a database and process results
Create a DAG that uses S3Hook to check if a file exists before downloading
Create a DAG that uses HttpHook to call an external REST API
Create a custom Hook for an internal API that is not natively supported
Create a DAG that uses MySqlHook to insert processed data into a table

---
### TaskFlow API
Rewrite a traditional PythonOperator DAG using TaskFlow API decorators
Create a TaskFlow DAG that chains 4 Python functions passing data between them
Create a TaskFlow DAG with branching using @task.branch decorator
Create a TaskFlow DAG that runs a task in a virtual environment with specific packages
Mix traditional operators and TaskFlow API tasks in the same DAG

---
### Dynamic DAGs
Generate 10 DAGs dynamically from a config file or dictionary
Create a DAG that dynamically generates tasks based on a list of tables
Create a DAG using expand() to process a list of files in parallel
Create a DAG factory pattern to generate similar DAGs for multiple clients
Create a DAG where number of tasks changes based on database query result

---
### Scheduling & Backfill
Create a DAG and manually trigger a backfill for the last 30 days using CLI
Create a DAG that handles late arriving data correctly using execution_date
Create a DAG with depends_on_past=True and test how it blocks when previous run fails
Create a DAG that uses data interval start and end correctly for incremental loads
Schedule a DAG using cron expression for last day of every month
Create a DAG that uses Dataset based scheduling instead of time based scheduling

---
### Error Handling & Alerting
Create a DAG that sends Slack notification on task failure
Create a DAG with task-level SLA and trigger an alert when SLA is missed
Create a DAG where on_failure_callback logs error details to a database
Create a DAG that has different retry strategies for different tasks
Create a DAG where failure of optional tasks does not block critical tasks

---
### SubDAGs & TaskGroups
Refactor a complex DAG into TaskGroups for better organization
Create a DAG with nested TaskGroups for multi-layer pipeline organization
Create a DAG with TaskGroup that has its own set of dependencies
Convert an old SubDAG pattern to a TaskGroup pattern
Create a TaskGroup for transformation tasks and another for loading tasks

---
### Pools & Concurrency
Create a Pool that limits database tasks to run only 3 at a time
Assign tasks from multiple DAGs to the same pool and observe queuing behavior
Configure a DAG to limit max 2 active runs at a time
Create a scenario where without pools you get database connection errors and fix it with pools
Prioritize critical tasks over non-critical tasks using priority_weight

---
### Executors
Set up Airflow with LocalExecutor and run parallel tasks
Set up CeleryExecutor with Redis and run tasks across multiple workers
Configure KubernetesExecutor and run each task in its own pod
Observe task behavior difference between SequentialExecutor and LocalExecutor
Configure different queues for different types of tasks in CeleryExecutor

---
### Real World ETL/ELT Scenarios
Build a DAG that extracts data from MySQL, transforms with Python, loads into PostgreSQL
Build a DAG that downloads files from S3, processes them, and loads into Redshift
Build a DAG that calls a REST API, paginates through results, and stores in a database
Build a DAG that runs dbt models after data is loaded into Snowflake
Build a DAG that reads from Kafka topic and loads into BigQuery
Build an incremental load DAG that only processes new records since last run
Build a DAG that handles CSV files landing in S3 and triggers processing pipeline
Build a DAG that orchestrates a Spark job on EMR and waits for completion
Build a full data pipeline DAG with data quality checks between each stage
Build a DAG that loads data into a staging table, validates, then moves to production table

---
### Data Quality & Validation
Create a DAG that validates row count before and after transformation
Create a DAG that checks for null values in critical columns and fails if found
Create a DAG that runs Great Expectations checks between pipeline stages
Create a DAG that compares source and target row counts and sends alert on mismatch
Create a DAG where data quality failure triggers a separate cleanup task

---
### Templating & Macros
Create a task that uses execution_date in a SQL query using Jinja templating
Create a DAG that passes dynamic file paths using ds macro
Create a DAG that uses prev_ds and next_ds to define data window
Create a custom macro and use it across multiple tasks
Create a parameterized DAG that accepts runtime parameters using params

---
### Secrets & Security
Store a database password in AWS Secrets Manager and retrieve it in a DAG
Configure Fernet key and encrypt connections in Airflow metadata DB
Configure RBAC and create a read-only user who can only view DAGs
Store API keys in HashiCorp Vault and access them from Airflow tasks
Create a DAG that retrieves secrets at runtime without exposing them in logs

---
### Monitoring & Debugging
Find why a DAG run is stuck in running state and resolve zombie tasks
Debug a task that is stuck in queued state and never executes
Analyze Gantt chart to find bottleneck tasks in a pipeline
Set up remote logging to S3 and access task logs from S3
Create a DAG that logs custom metrics to StatsD for Grafana monitoring
Investigate why a DAG is not being picked up by the scheduler

---
### Deployment & DevOps
Write a docker-compose file to run Airflow with CeleryExecutor locally
Deploy Airflow on Kubernetes using official Helm chart
Set up a CI/CD pipeline that validates DAGs before deploying to production
Write a test for a DAG to verify task count and dependencies are correct
Handle DAG versioning when modifying a DAG that has active runs
Migrate DAGs and connections from one Airflow environment to another

---
### Performance & Optimization
Identify why DAGs are taking long to load and fix by optimizing DAG file
Identify a DAG that is hammering the database and fix with connection pooling
Optimize a DAG that processes 1000 files by using dynamic task mapping
Tune scheduler settings for an environment with 500+ DAGs
Reduce XCom size by storing large data in S3 and passing only the path

---
### Interview / Troubleshooting Scenarios
A DAG ran successfully but data was not loaded - how do you debug
A task is running but taking 10x longer than usual - what do you check
Two DAGs are writing to the same table causing conflicts - how do you fix
A DAG is scheduled but never runs - list all possible reasons
Your DAG worked in development but fails in production - what do you investigate
A sensor has been running for 48 hours without triggering - what do you do
After upgrading Airflow version, DAGs are broken - how do you approach the fix
You need to reprocess last 6 months of data without affecting current runs