## AWS EMR Operators

| Operator | Definition |
| :-- | :-- |
| EmrCreateJobFlowOperator | Creates and starts a new EMR cluster with specified configurations. Returns the cluster Job Flow ID for use in downstream tasks. |
| EmrAddStepsOperator | Submits one or more steps (Spark, Hive, Pig jobs) to a running EMR cluster. Returns step IDs that can be used by sensors to monitor progress. |
| EmrStepSensor | Waits and monitors an EMR step until it reaches a terminal state (completed/failed). Keeps polling the step status at defined intervals. |
| EmrJobFlowSensor | Waits for an EMR cluster itself to reach a specific state like WAITING or RUNNING. Commonly used after cluster creation to confirm it is ready. |
| EmrTerminateJobFlowOperator | Shuts down and terminates a running EMR cluster. Typically used as the last task in a pipeline to avoid unnecessary costs. |
| EmrContainerOperator | Submits a job to EMR on EKS (Kubernetes based EMR). Used when running EMR workloads on Kubernetes infrastructure. |
| EmrServerlessCreateApplicationOperator | Creates an EMR Serverless application for running Spark or Hive jobs without managing clusters. No infrastructure provisioning needed. |
| EmrServerlessStartJobRunOperator | Submits and starts a job run on an existing EMR Serverless application. Used as a fully serverless alternative to traditional EMR cluster steps. |
| EmrServerlessJobSensor | Monitors and waits for an EMR Serverless job run to complete. Polls job status until success or failure state is reached. |

```
EmrCreateJobFlowOperator        → spin up cluster
       ↓
EmrJobFlowSensor                → wait for cluster to be ready
       ↓
EmrAddStepsOperator             → submit spark job
       ↓
EmrStepSensor                   → wait for job to finish
       ↓
EmrTerminateJobFlowOperator     → shut down cluster
```


```
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.emr import (
    EmrCreateJobFlowOperator,
    EmrAddStepsOperator,
    EmrTerminateJobFlowOperator
)
from airflow.providers.amazon.aws.sensors.emr import (
    EmrJobFlowSensor,
    EmrStepSensor
)
from airflow.utils.email import send_email
from datetime import datetime, timedelta


# ── Alert Config ───────────────────────────────────────
COMMON_DL = "data-engineering-dl@company.com"
EMR_DL    = "emr-team-dl@company.com"

TASK_ALERT_CONFIG = {
    "create_emr_cluster"      : [EMR_DL],
    "wait_for_cluster"        : [EMR_DL],
    "submit_extraction_job"   : [EMR_DL],
    "wait_for_extraction"     : [EMR_DL],
    "submit_transformation_job": [EMR_DL],
    "wait_for_transformation" : [EMR_DL],
    "submit_aggregation_job"  : [EMR_DL],
    "wait_for_aggregation"    : [EMR_DL],
    "terminate_cluster"       : [EMR_DL],
}

def build_email_body(context):
    return f"""
        <h3>EMR Pipeline Failure Alert</h3>
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
    task_id      = context['task_instance'].task_id
    dag_id       = context['dag'].dag_id
    task_dl      = TASK_ALERT_CONFIG.get(task_id, [])
    recipients   = list(set(task_dl + [COMMON_DL]))
    subject      = f"❌ EMR Pipeline Failed | DAG: {dag_id} | Task: {task_id}"
    send_email(to=recipients, subject=subject, html_content=build_email_body(context))

def success_alert(context):
    dag_id = context['dag'].dag_id
    send_email(
        to=[COMMON_DL],
        subject=f"✅ EMR Pipeline Completed | DAG: {dag_id}",
        html_content=f"<h3>Pipeline {dag_id} completed successfully on {context['execution_date']}</h3>"
    )


# ── Cluster Config ─────────────────────────────────────
EMR_CLUSTER_CONFIG = {
    "Name"          : "emr-etl-cluster",
    "ReleaseLabel"  : "emr-6.10.0",
    "Applications"  : [{"Name": "Spark"}, {"Name": "Hadoop"}],
    "Instances"     : {
        "InstanceGroups": [
            {
                "Name"          : "Master",
                "Market"        : "ON_DEMAND",
                "InstanceRole"  : "MASTER",
                "InstanceType"  : "m5.xlarge",
                "InstanceCount" : 1
            },
            {
                "Name"          : "Workers",
                "Market"        : "SPOT",
                "InstanceRole"  : "CORE",
                "InstanceType"  : "m5.2xlarge",
                "InstanceCount" : 3
            }
        ],
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected"       : False
    },
    "JobFlowRole"   : "EMR_EC2_DefaultRole",
    "ServiceRole"   : "EMR_DefaultRole",
    "LogUri"        : "s3://my-bucket/emr-logs/",
    "Tags"          : [{"Key": "Environment", "Value": "production"}]
}


# ── Spark Steps ────────────────────────────────────────
EXTRACTION_STEP = [{
    "Name"           : "Extraction Job",
    "ActionOnFailure": "CONTINUE",
    "HadoopJarStep"  : {
        "Jar" : "command-runner.jar",
        "Args": [
            "spark-submit",
            "--deploy-mode", "cluster",
            "--master"     , "yarn",
            "s3://my-bucket/scripts/extraction.py",
            "--date"       , "{{ ds }}"
        ]
    }
}]

TRANSFORMATION_STEP = [{
    "Name"           : "Transformation Job",
    "ActionOnFailure": "CONTINUE",
    "HadoopJarStep"  : {
        "Jar" : "command-runner.jar",
        "Args": [
            "spark-submit",
            "--deploy-mode", "cluster",
            "--master"     , "yarn",
            "--conf"       , "spark.executor.memory=4g",
            "s3://my-bucket/scripts/transformation.py",
            "--date"       , "{{ ds }}"
        ]
    }
}]

AGGREGATION_STEP = [{
    "Name"           : "Aggregation Job",
    "ActionOnFailure": "CONTINUE",
    "HadoopJarStep"  : {
        "Jar" : "command-runner.jar",
        "Args": [
            "spark-submit",
            "--deploy-mode", "cluster",
            "--master"     , "yarn",
            "s3://my-bucket/scripts/aggregation.py",
            "--date"       , "{{ ds }}"
        ]
    }
}]


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
    dag_id="emr_end_to_end_pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    on_success_callback=success_alert,
    tags=["emr", "etl", "production"]
) as dag:

    start = EmptyOperator(task_id="start")

    # ── Step 1 Create Cluster ──────────────────────────
    create_cluster = EmrCreateJobFlowOperator(
        task_id="create_emr_cluster",
        job_flow_overrides=EMR_CLUSTER_CONFIG,
        aws_conn_id="aws_default"
    )

    # ── Step 2 Wait for Cluster ────────────────────────
    wait_for_cluster = EmrJobFlowSensor(
        task_id="wait_for_cluster",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        target_states=["WAITING"],
        failed_states=["TERMINATING", "TERMINATED", "TERMINATED_WITH_ERRORS"],
        aws_conn_id="aws_default",
        mode="reschedule"
    )

    # ── Step 3 Submit Extraction Job ───────────────────
    submit_extraction = EmrAddStepsOperator(
        task_id="submit_extraction_job",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        steps=EXTRACTION_STEP,
        aws_conn_id="aws_default"
    )

    wait_for_extraction = EmrStepSensor(
        task_id="wait_for_extraction",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull('submit_extraction_job', key='return_value')[0] }}",
        target_states=["COMPLETED"],
        failed_states=["CANCELLED", "FAILED", "INTERRUPTED"],
        aws_conn_id="aws_default",
        mode="reschedule"
    )

    # ── Step 4 Submit Transformation Job ──────────────
    submit_transformation = EmrAddStepsOperator(
        task_id="submit_transformation_job",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        steps=TRANSFORMATION_STEP,
        aws_conn_id="aws_default"
    )

    wait_for_transformation = EmrStepSensor(
        task_id="wait_for_transformation",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull('submit_transformation_job', key='return_value')[0] }}",
        target_states=["COMPLETED"],
        failed_states=["CANCELLED", "FAILED", "INTERRUPTED"],
        aws_conn_id="aws_default",
        mode="reschedule"
    )

    # ── Step 5 Submit Aggregation Job ─────────────────
    submit_aggregation = EmrAddStepsOperator(
        task_id="submit_aggregation_job",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        steps=AGGREGATION_STEP,
        aws_conn_id="aws_default"
    )

    wait_for_aggregation = EmrStepSensor(
        task_id="wait_for_aggregation",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull('submit_aggregation_job', key='return_value')[0] }}",
        target_states=["COMPLETED"],
        failed_states=["CANCELLED", "FAILED", "INTERRUPTED"],
        aws_conn_id="aws_default",
        mode="reschedule"
    )

    # ── Step 6 Terminate Cluster ───────────────────────
    terminate_cluster = EmrTerminateJobFlowOperator(
        task_id="terminate_cluster",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        aws_conn_id="aws_default",
        trigger_rule="all_done"   # terminate even if steps fail
    )

    end = EmptyOperator(task_id="end")

    # ── Dependencies ───────────────────────────────────
    (
        start
        >> create_cluster
        >> wait_for_cluster
        >> submit_extraction
        >> wait_for_extraction
        >> submit_transformation
        >> wait_for_transformation
        >> submit_aggregation
        >> wait_for_aggregation
        >> terminate_cluster
        >> end
    )

```

```
EMR Pipeline
─────────────────────────────────────────────────
Create Cluster → Wait → Extract → Wait
→ Transform → Wait → Aggregate → Wait
→ Terminate Cluster
```