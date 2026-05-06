-  What is Apache airflow?
- Is Apache Airflow an ETL tool? (No, it is an orchestration tool)
- How do we define workflows in Apache Airflow? (Explain DAG and tasks)
- What are the components of the Apache Airflow architecture? ( Scheduler, Executor, Webserver, Metadata storage datbase, workers)
- What are Local Executors and their types in Airflow?
- What is a Celery Executor ?
- How is Kubernetes Executor different from Celery Executor?
- What are Variables (Variable Class) in Apache Airflow?
- What is the purpose of Airflow XComs?
- Why don't we use Variables instead of Airflow XComs, and how are they different?

---

- What are the states a Task can be in? Define an ideal task flow. (scheduled,success, failure, queued , skipped etc)
- What is the role of Airflow Operators?
- How does airflow communicate with a third party (S3, Postgres, MySQL)? (using hooks)
- What are the basic steps to create a DAG? (define dag, task, dependency)
- What is Branching in Directed Acyclic Graphs (DAGs)?
- What are ways to Control Airflow Workflow? (Branching , Latest Only (LatestOnlyOperator),Depends on Past (depends_on_past = true; arg), trigger rules ("trigger_rule"; arg))

    - Branching (BranchPythonOperator): We can apply multiple branches or conditional limits to what path the flow should go after this task.

    - Latest Only (LatestOnlyOperator): This task will only run if the date the DAG is running is on the current data. It will help in cases when you have a few tasks which you don't want to run while backfilling historical data.

    - Depends on Past (depends_on_past = true; arg): Will only run if this task run succeeded in the previous DAG run.

    - Trigger rules ("trigger_rule"; arg): By default, a DAG will only run an airflow task when all of its previous tasks have succeeded, but trigger rules can help us alter those conditions. Like "trigger_rule = always" to run it anyways, irrespective of if the previous tasks succeeded or not, OR "trigger_rule = all_success" to run it only when all of its previous jobs succeed.

- Explain the External task Sensor? (We can Define an ExternalTaskSensor in DAG_B if we want DAG_B to wait for the completion of DAG_A for a specific execution date)
- What are the ways to monitor Apache Airflow? (logs, DAG view)
- What is TaskFlow API? and how is it helpful?
- How are Connections used in Apache Airflow?

---

- Explain Dynamic DAGs
- What are some of the most useful Airflow CLI commands?
- How to control the parallelism or concurrency of tasks in Apache Airflow configuration? (confifurations in dag definition: max_active_tasks_per_dag, parallelism,max_active_runs_per_dag,concurrency,max_active_runs )
- What do you understand by Jinja Templating?
- What are Macros in Airflow?
- What are the limitations of TaskFlow API?
    - Missing package dependency management, the TaskFlow abstraction can only work if everybody in the organization agrees to use the same package versions and other airflow dependencies, which makes TaskFlow not so ready for heavy production loads.

    - Another limit is that TaskFlow API is built upon XComs, and XComs don't provide proper data-sharing functionality. Instead, it provides an abstraction to only share small amounts of data between tasks.

- How is the Executor involved in the Airflow Life cycle?
- List the types of Trigger rules.
- Deadline alerts
- What is a Spark Submit Operator?
- What is a Spark JDBC Operator?
- What is the SparkSQL operator?

---

- How would you approach if you wanted to queue up multiple dags with order dependencies?
- What if your Apache Airflow DAG failed for the last ten days, and now you want to backfill those last ten days' data, but you don't need to run all the tasks of the dag to backfill the data?
- What will happen if you set 'catchup=False' in the dag and 'latest_only = True' for some of the dag tasks?
- What if you need to use a set of functions to be used in a directed acyclic graph?
- How would you handle a task which has no dependencies on any other tasks? ( We can set "trigger_rules = 'always'" in a task, which will make sure the task will run irrespective of if the previous tasks have succeeded or not.)

- What would you do if you wanted to create multiple dags with similar functionalities but with different arguments? (Dynamic DAGS)
- If we want to exchange large amounts of data, what is the solution to the limitation of XComs?
    - Since Airflow is an orchestrator tool and not a data processing framework, if we want to process large gigabytes of data with Airflow, we use Spark (which is an open-source distributed system for large-scale data processing) along with the Airflow DAGs because of all the optimizations that It brings to the table.