## Glue operators

| Operator | Definition |
| :-- | :-- |
| GlueJobOperator | Triggers an AWS Glue ETL job and optionally waits for its completion. Can pass job arguments dynamically at runtime. |
| GlueJobSensor | Monitors a running Glue job and waits until it finishes successfully or fails. Useful when GlueJobOperator is run without wait_for_completion. |
| GlueCrawlerOperator | Triggers an AWS Glue Crawler to scan data sources and update the Glue Data Catalog with schema information. |
| GlueCrawlerSensor | Waits and monitors a Glue Crawler run until it completes. Used after GlueCrawlerOperator to confirm catalog is updated before querying. |
| GlueDataQualityOperator | Runs AWS Glue Data Quality rules against a dataset and evaluates results. Used to validate data before moving to downstream pipeline. |
| AthenaOperator | Executes a SQL query on AWS Athena which reads data from S3 via Glue Catalog. Returns a query execution ID for monitoring. |
| AthenaSensor | Waits for an Athena query to complete execution. Used after AthenaOperator to confirm query is done before processing results. |

```
GlueCrawlerOperator             → crawl raw data in S3
       ↓
GlueCrawlerSensor               → wait for catalog update
       ↓
GlueJobOperator                 → run ETL transformation
       ↓
GlueJobSensor                   → wait for job completion
       ↓
AthenaOperator                  → query transformed data
```


```
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor
from airflow.providers.amazon.aws.sensors.glue_crawler import GlueCrawlerSensor
from airflow.providers.amazon.aws.sensors.athena import AthenaSensor
from airflow.utils.email import send_email
from datetime import datetime, timedelta


# ── Alert Config ───────────────────────────────────────
COMMON_DL = "data-engineering-dl@company.com"
GLUE_DL   = "glue-team-dl@company.com"

TASK_ALERT_CONFIG = {
    "crawl_raw_data"          : [GLUE_DL],
    "wait_for_raw_crawler"    : [GLUE_DL],
    "run_glue_ingestion_job"  : [GLUE_DL],
    "wait_for_ingestion"      : [GLUE_DL],
    "run_glue_transform_job"  : [GLUE_DL],
    "wait_for_transform"      : [GLUE_DL],
    "crawl_processed_data"    : [GLUE_DL],
    "wait_for_processed_crawler": [GLUE_DL],
    "run_athena_validation"   : [GLUE_DL],
    "wait_for_athena"         : [GLUE_DL],
}

def build_email_body(context):
    return f"""
        <h3>Glue Pipeline Failure Alert</h3>
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
    subject    = f"❌ Glue Pipeline Failed | DAG: {dag_id} | Task: {task_id}"
    send_email(to=recipients, subject=subject, html_content=build_email_body(context))

def success_alert(context):
    dag_id = context['dag'].dag_id
    send_email(
        to=[COMMON_DL],
        subject=f"✅ Glue Pipeline Completed | DAG: {dag_id}",
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
    dag_id="glue_end_to_end_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    on_success_callback=success_alert,
    tags=["glue", "etl", "production"]
) as dag:

    start = EmptyOperator(task_id="start")

    # ── Step 1 Crawl Raw Data in S3 ───────────────────
    crawl_raw = GlueCrawlerOperator(
        task_id="crawl_raw_data",
        config={"Name": "raw-data-crawler"},
        aws_conn_id="aws_default"
    )

    wait_for_raw_crawler = GlueCrawlerSensor(
        task_id="wait_for_raw_crawler",
        crawler_name="raw-data-crawler",
        aws_conn_id="aws_default",
        mode="reschedule",
        poke_interval=30
    )

    # ── Step 2 Run Glue Ingestion Job ─────────────────
    run_ingestion = GlueJobOperator(
        task_id="run_glue_ingestion_job",
        job_name="glue-ingestion-job",
        script_args={
            "--execution_date": "{{ ds }}",
            "--source_bucket" : "s3://my-bucket/raw/",
            "--target_bucket" : "s3://my-bucket/staging/",
            "--env"           : "production"
        },
        aws_conn_id="aws_default",
        wait_for_completion=False   # we use sensor to wait
    )

    wait_for_ingestion = GlueJobSensor(
        task_id="wait_for_ingestion",
        job_name="glue-ingestion-job",
        run_id="{{ task_instance.xcom_pull('run_glue_ingestion_job') }}",
        aws_conn_id="aws_default",
        mode="reschedule",
        poke_interval=60
    )

    # ── Step 3 Run Glue Transformation Job ────────────
    run_transform = GlueJobOperator(
        task_id="run_glue_transform_job",
        job_name="glue-transform-job",
        script_args={
            "--execution_date" : "{{ ds }}",
            "--source_bucket"  : "s3://my-bucket/staging/",
            "--target_bucket"  : "s3://my-bucket/processed/",
            "--partition_key"  : "{{ ds }}"
        },
        aws_conn_id="aws_default",
        wait_for_completion=False
    )

    wait_for_transform = GlueJobSensor(
        task_id="wait_for_transform",
        job_name="glue-transform-job",
        run_id="{{ task_instance.xcom_pull('run_glue_transform_job') }}",
        aws_conn_id="aws_default",
        mode="reschedule",
        poke_interval=60
    )

    # ── Step 4 Crawl Processed Data ───────────────────
    crawl_processed = GlueCrawlerOperator(
        task_id="crawl_processed_data",
        config={"Name": "processed-data-crawler"},
        aws_conn_id="aws_default"
    )

    wait_for_processed_crawler = GlueCrawlerSensor(
        task_id="wait_for_processed_crawler",
        crawler_name="processed-data-crawler",
        aws_conn_id="aws_default",
        mode="reschedule",
        poke_interval=30
    )

    # ── Step 5 Run Athena Validation Query ────────────
    run_athena_validation = AthenaOperator(
        task_id="run_athena_validation",
        query="""
            SELECT
                COUNT(*)        AS total_records,
                COUNT(DISTINCT id) AS unique_records,
                MAX(updated_at) AS latest_record
            FROM processed_db.orders
            WHERE partition_date = '{{ ds }}'
        """,
        database="processed_db",
        output_location="s3://my-bucket/athena-results/",
        aws_conn_id="aws_default"
    )

    wait_for_athena = AthenaSensor(
        task_id="wait_for_athena",
        query_execution_id="{{ task_instance.xcom_pull('run_athena_validation') }}",
        aws_conn_id="aws_default",
        mode="reschedule",
        poke_interval=15
    )

    end = EmptyOperator(task_id="end")

    # ── Dependencies ───────────────────────────────────
    (
        start
        >> crawl_raw
        >> wait_for_raw_crawler
        >> run_ingestion
        >> wait_for_ingestion
        >> run_transform
        >> wait_for_transform
        >> crawl_processed
        >> wait_for_processed_crawler
        >> run_athena_validation
        >> wait_for_athena
        >> end
    )
```


```
Glue Pipeline
─────────────────────────────────────────────────
Crawl Raw S3 → Wait → Ingestion Job → Wait
→ Transform Job → Wait → Crawl Processed
→ Wait → Athena Validation → Wait
```