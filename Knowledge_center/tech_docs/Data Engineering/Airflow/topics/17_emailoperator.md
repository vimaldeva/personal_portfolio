## EmailOperator
- Sends an email from a task
- Requires SMTP configuration in airflow.cfg

SMTP Setup in airflow.cfg
```
[smtp]
smtp_host = smtp.gmail.com
smtp_port = 587
smtp_user = your@gmail.com
smtp_password = yourpassword
smtp_mail_from = your@gmail.com
```

```
from airflow.operators.email import EmailOperator

# Basic email
task = EmailOperator(
    task_id="send_email",
    to="team@company.com",
    subject="Pipeline Completed",
    html_content="<h3>DAG ran successfully</h3>"
)

# Email with dynamic content using templating
task = EmailOperator(
    task_id="send_report_email",
    to=["manager@company.com", "team@company.com"],
    subject="Daily Report - {{ ds }}",
    html_content="""
        <h3>Daily Pipeline Report</h3>
        <p>Date: {{ ds }}</p>
        <p>Status: Success</p>
    """
)
```

Most Common Pattern → Email on Failure

```
default_args = {
    "email": ["alerts@company.com"],
    "email_on_failure": True,
    "email_on_retry": False
}

with DAG(
    dag_id="my_dag",
    default_args=default_args,
    ...
) as dag:
    pass
```



