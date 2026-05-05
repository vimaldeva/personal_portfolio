## Hook
- An interface to connect to external systems
- Manages connection logic internally
- Operators and Tasks use Hooks under the hood
- Uses Airflow Connections to get credentials
- Reusable across multiple DAGs


```
from airflow.providers.postgres.hooks.postgres import PostgresHook

def query_database():
    hook = PostgresHook(postgres_conn_id="my_postgres_conn")
    records = hook.get_records("SELECT * FROM users")
    print(records)
```

| Hook | Connects To |
| :-- | :-- |
| PostgresHook | PostgreSQL |
| MySqlHook | MySQL |
| S3Hook | AWS S3 |
| HttpHook | REST APIs |
| BigQueryHook | Google BigQuery |
| SlackHook | Slack |


Operator vs Hook

- Hook → handles the connection
- Operator → handles the action/logic
- Operator uses Hook internally to connect and execute