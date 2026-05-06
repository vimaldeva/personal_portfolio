
```
from airflow import DAG
from airflow.providers.amazon.aws.operators.emr import EmrAddStepsOperator
from airflow.providers.amazon.aws.sensors.emr import EmrStepSensor
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.email import send_email
from datetime import datetime, timedelta


# ── Callback ──────────────────────────────────────────
def failure_alert(context):
    dag_id         = context['dag'].dag_id
    task_id        = context['task_instance'].task_id
    execution_date = context['execution_date']
    log_url        = context['task_instance'].log_url
    exception      = context.get('exception')

    subject = f"❌ Pipeline Failed | DAG: {dag_id} | Task: {task_id}"

    body = f"""
        <h3>Pipeline Failure Alert</h3>
        <table>
            <tr><td><b>DAG</b></td><td>{dag_id}</td></tr>
            <tr><td><b>Failed Task</b></td><td>{task_id}</td></tr>
            <tr><td><b>Execution Date</b></td><td>{execution_date}</td></tr>
            <tr><td><b>Error</b></td><td>{exception}</td></tr>
            <tr><td><b>Log URL</b></td><td><a href="{log_url}">Click Here</a></td></tr>
        </table>
        <p>Please investigate immediately.</p>
    """

    send_email(
        to=["data-engineering-dl@company.com"],
        subject=subject,
        html_content=body
    )


# ── Default Args ──────────────────────────────────────
default_args = {
    "owner"              : "data-engineering",
    "retries"            : 2,
    "retry_delay"        : timedelta(minutes=5),
    "on_failure_callback": failure_alert,
    "email_on_failure"   : False,
    "email_on_retry"     : False
}


# ── DAG ───────────────────────────────────────────────
with DAG(
    dag_id="emr_databricks_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    start = EmptyOperator(task_id="start")

    # EMR Job
    emr_step = EmrAddStepsOperator(
        task_id="submit_emr_job",
        job_flow_id="j-XXXXXXXXXX",
        steps=[{
            "Name": "Spark ETL Job",
            "ActionOnFailure": "CONTINUE",
            "HadoopJarStep": {
                "Jar": "command-runner.jar",
                "Args": ["spark-submit", "/scripts/etl.py"]
            }
        }]
    )

    emr_sensor = EmrStepSensor(
        task_id="wait_for_emr_job",
        job_flow_id="j-XXXXXXXXXX",
        step_id="{{ task_instance.xcom_pull('submit_emr_job')[0] }}",
        mode="reschedule"
    )

    # Databricks Job
    databricks_job = DatabricksRunNowOperator(
        task_id="submit_databricks_job",
        databricks_conn_id="databricks_default",
        job_id=12345
    )

    end = EmptyOperator(task_id="end")

    start >> emr_step >> emr_sensor >> databricks_job >> end

```