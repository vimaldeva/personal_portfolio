## TaskFlow
If you write most of your Dags using plain Python code rather than Operators, then the TaskFlow API will make it much easier to author clean Dags without extra boilerplate, all using the @task decorator.

TaskFlow takes care of moving inputs and outputs between your Tasks using XComs for you, as well as automatically calculating dependencies - when you call a TaskFlow function in your Dag file, rather than executing it, you will get an object representing the XCom for the result (an XComArg), that you can then use as inputs to downstream tasks or operators. For example:

```
from airflow.sdk import task
from airflow.providers.smtp.operators.smtp import EmailOperator

@task
def get_ip():
    return my_ip_service.get_main_ip()

@task(multiple_outputs=True)
def compose_email(external_ip):
    return {
        'subject':f'Server connected from {external_ip}',
        'body': f'Your server executing Airflow is connected from the external IP {external_ip}<br>'
    }

email_info = compose_email(get_ip())

EmailOperator(
    task_id='send_email_notification',
    to='example@example.com',
    subject=email_info['subject'],
    html_content=email_info['body']
)
``` 

Here, there are three tasks - get_ip, compose_email, and send_email_notification.

The first two are declared using TaskFlow, and automatically pass the return value of get_ip into compose_email, not only linking the XCom across, but automatically declaring that compose_email is downstream of get_ip.

```
@task
def hello_name(name: str):
    print(f'Hello {name}!')

hello_name('Airflow users')
``` 

### Context
You can access Airflow context variables by adding them as keyword arguments as shown in the following example:

```
from airflow.models.taskinstance import TaskInstance
from airflow.models.dagrun import DagRun


@task
def print_ti_info(task_instance: TaskInstance, dag_run: DagRun):
    print(f"Run ID: {task_instance.run_id}")  # Run ID: scheduled__2023-08-09T00:00:00+00:00
    print(f"Duration: {task_instance.duration}")  # Duration: 0.972019
    print(f"Dag Run queued at: {dag_run.queued_at}")  # 2023-08-10 00:00:01+02:20
```

Alternatively, you may add **kwargs to the signature of your task and all Airflow context variables will be accessible in the kwargs dict:

```
from airflow.models.taskinstance import TaskInstance
from airflow.models.dagrun import DagRun


@task
def print_ti_info(**kwargs):
    ti: TaskInstance = kwargs["task_instance"]
    print(f"Run ID: {ti.run_id}")  # Run ID: scheduled__2023-08-09T00:00:00+00:00
    print(f"Duration: {ti.duration}")  # Duration: 0.972019

    dr: DagRun = kwargs["dag_run"]
    print(f"Dag Run queued at: {dr.queued_at}")  # 2023-08-10 00:00:01+02:20
```

