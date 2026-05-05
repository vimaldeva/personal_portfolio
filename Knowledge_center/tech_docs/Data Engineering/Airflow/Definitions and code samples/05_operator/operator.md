## Operators
An Operator is conceptually a template for a predefined Task, that you can just define declaratively inside your Dag:

```
with DAG("my-dag") as dag:
    ping = HttpOperator(endpoint="http://example.com/update/")
    email = EmailOperator(to="admin@example.com", subject="Update complete")

    ping >> email
```

Airflow has a very extensive set of operators available, with some built-in to the core or pre-installed providers. Some popular operators from core include:

- BashOperator - executes a bash command
- PythonOperator - calls an arbitrary Python function

Use the @task decorator to execute an arbitrary Python function. It doesn’t support rendering jinja templates passed as arguments.

Some popular operators from here include:

- EmailOperator
- HttpOperator
- SQLExecuteQueryOperator
- DockerOperator
- HiveOperator
- S3FileTransformOperator
- PrestoToMySqlOperator
- SlackAPIOperator

### Jinja Templating

Airflow leverages the power of Jinja Templating and this can be a powerful tool to use in combination with macros.



```
# The start of the data interval as YYYY-MM-DD
date = "{{ ds }}"
t = BashOperator(
    task_id="test_env",
    bash_command="/tmp/test.sh ",
    dag=dag,
    env={"DATA_INTERVAL_START": date},
)
```

For example, consider a BashOperator which runs a multi-line bash script, this will load the file at script.sh and use its contents as the value for bash_command:

```
run_script = BashOperator(
    task_id="run_script",
    bash_command="script.sh",
)
```

