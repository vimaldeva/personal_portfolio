## Databricks operator

| Operator | Definition |
| :-- | :-- |
| DatabricksRunNowOperator | Triggers an existing Databricks Job by Job ID and waits for it to complete. Most commonly used operator for running pre-configured Databricks jobs. |
| DatabricksSubmitRunOperator | Submits a one-time Databricks run with custom notebook, JAR or Python script configuration. Used when job config is defined dynamically in Airflow. |
| DatabricksCreateJobsOperator | Creates or updates a Databricks job definition programmatically from Airflow. Useful for managing job configurations as code. |
| DatabricksRunNowDeferrableOperator | Deferrable version of DatabricksRunNowOperator that releases the worker slot while waiting. More efficient for long running Databricks jobs. |
| DatabricksSubmitRunDeferrableOperator | Deferrable version of DatabricksSubmitRunOperator that frees up worker resources during job execution. Best for large scale pipelines with many concurrent jobs. |
| DatabricksNotebookOperator | Runs a specific Databricks notebook as a task with optional parameters passed at runtime. Useful for running notebooks directly without a pre-defined job. |
| DatabricksSensor | Monitors a Databricks run and waits until it reaches a terminal state. Used when job is triggered outside Airflow and just needs monitoring. |
| DatabricksCopyIntoOperator | Executes a Databricks COPY INTO SQL command to load data from cloud storage into a Delta table. Used for incremental data ingestion into Delta Lake. |
| DatabricksReposCreateOperator | Creates a new Databricks Repo connected to a Git repository. Used for managing notebook code versions in CI/CD pipelines. |
| DatabricksRepoUpdateOperator | Updates an existing Databricks Repo to a specific branch, tag or commit. Used in CI/CD pipelines to deploy latest code before running jobs. |


```

DatabricksRepoUpdateOperator    → pull latest code from Git
       ↓
DatabricksRunNowOperator        → trigger ingestion job
       ↓
DatabricksRunNowOperator        → trigger transformation job
       ↓
DatabricksRunNowOperator        → trigger aggregation job

```

```
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.databricks.operators.databricks import (
    DatabricksRunNowOperator,
    DatabricksSubmitRunOperator
)
from airflow.utils.email import send_email
from datetime import datetime, timedelta


# ── Alert Config ───────────────────────────────────────
COMMON_DL       = "data-engineering-dl@company.com"
DATABRICKS_DL   = "databricks-team-dl@company.com"

TASK_ALERT_CONFIG = {
    "update_repo"             : [DATABRICKS_DL],
    "run_ingestion_job"       : [DATABRICKS_DL],
    "run_transformation_job"  : [DATABRICKS_DL],
    "run_aggregation_job"     : [DATABRICKS_DL],
    "run_data_quality_checks" : [DATABRICKS_DL],
    "run_export_job"          : [DATABRICKS_DL],
}

def build_email_body(context):
    return f"""
        <h3>Databricks Pipeline Failure Alert</h3>
        <table>
            <tr><td><b>DAG</b></td>
                <td>{context['dag'].dag_id}</td></tr>
            <tr><td><b>Failed Task</b></td>
                <td>{context['task_instance'].task_id}</td></tr>
            <tr><td><b>Execution Date</b></td>
                <td>{context['execution_date']}</td></tr>
            <tr><td><b>Retry Number</b></td>
                <td>{context['task_instance'].try_number}</td></tr>
            <tr><td><b>Error</b></td>
                <td>{context.get('exception')}</td></tr>
            <tr><td><b>Log URL</b></td>
                <td><a href="{context['task_instance'].log_url}">Click Here</a></td></tr>
        </table>
    """

def failure_alert(context):
    task_id    = context['task_instance'].task_id
    dag_id     = context['dag'].dag_id
    task_dl    = TASK_ALERT_CONFIG.get(task_id, [])
    recipients = list(set(task_dl + [COMMON_DL]))
    subject    = f"❌ Databricks Pipeline Failed | DAG: {dag_id} | Task: {task_id}"
    send_email(to=recipients, subject=subject, html_content=build_email_body(context))

def success_alert(context):
    dag_id = context['dag'].dag_id
    send_email(
        to=[COMMON_DL],
        subject=f"✅ Databricks Pipeline Completed | DAG: {dag_id}",
        html_content=f"<h3>Pipeline {dag_id} completed successfully on {context['execution_date']}</h3>"
    )


# ── Default Args ───────────────────────────────────────
default_args = {
    "owner"              : "data-engineering",
    "retries"            : 1,
    "retry_delay"        : timedelta(minutes=10),
    "on_failure_callback": failure_alert,
    "email_on_failure"   : False,
    "email_on_retry"     : False
}


# ── DAG ───────────────────────────────────────────────
with DAG(
    dag_id="databricks_end_to_end_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    on_success_callback=success_alert,
    tags=["databricks", "etl", "production"]
) as dag:

    start = EmptyOperator(task_id="start")

    # ── Step 1 Update Repo with Latest Code ───────────
    update_repo = DatabricksSubmitRunOperator(
        task_id="update_repo",
        databricks_conn_id="databricks_default",
        json={
            "run_name"  : "update-repo-{{ ds }}",
            "new_cluster": {
                "spark_version" : "13.3.x-scala2.12",
                "node_type_id"  : "i3.xlarge",
                "num_workers"   : 1
            },
            "notebook_task": {
                "notebook_path" : "/Repos/production/pipeline/utils/update_repo",
                "base_parameters": {
                    "branch": "main",
                    "date"  : "{{ ds }}"
                }
            }
        }
    )

    # ── Step 2 Run Ingestion Job ───────────────────────
    run_ingestion = DatabricksRunNowOperator(
        task_id="run_ingestion_job",
        databricks_conn_id="databricks_default",
        job_id=1001,
        notebook_params={
            "execution_date" : "{{ ds }}",
            "source_path"    : "s3://my-bucket/raw/{{ ds }}/",
            "target_schema"  : "bronze",
            "env"            : "production"
        }
    )

    # ── Step 3 Run Transformation Job ─────────────────
    run_transformation = DatabricksRunNowOperator(
        task_id="run_transformation_job",
        databricks_conn_id="databricks_default",
        job_id=1002,
        notebook_params={
            "execution_date" : "{{ ds }}",
            "source_schema"  : "bronze",
            "target_schema"  : "silver",
            "partition_date" : "{{ ds }}"
        }
    )

    # ── Step 4 Run Aggregation Job ─────────────────────
    run_aggregation = DatabricksRunNowOperator(
        task_id="run_aggregation_job",
        databricks_conn_id="databricks_default",
        job_id=1003,
        notebook_params={
            "execution_date" : "{{ ds }}",
            "source_schema"  : "silver",
            "target_schema"  : "gold",
            "aggregation_type": "daily"
        }
    )

    # ── Step 5 Run Data Quality Checks ────────────────
    run_dq_checks = DatabricksRunNowOperator(
        task_id="run_data_quality_checks",
        databricks_conn_id="databricks_default",
        job_id=1004,
        notebook_params={
            "execution_date" : "{{ ds }}",
            "schema"         : "gold",
            "table"          : "orders_aggregated",
            "dq_rules_path"  : "/configs/dq_rules.json"
        }
    )

    # ── Step 6 Export to Target System ────────────────
    run_export = DatabricksRunNowOperator(
        task_id="run_export_job",
        databricks_conn_id="databricks_default",
        job_id=1005,
        notebook_params={
            "execution_date" : "{{ ds }}",
            "source_schema"  : "gold",
            "target_db"      : "redshift_prod",
            "target_table"   : "orders_daily_summary"
        }
    )

    end = EmptyOperator(task_id="end")

    # ── Dependencies ───────────────────────────────────
    (
        start
        >> update_repo
        >> run_ingestion
        >> run_transformation
        >> run_aggregation
        >> run_dq_checks
        >> run_export
        >> end
    )

```