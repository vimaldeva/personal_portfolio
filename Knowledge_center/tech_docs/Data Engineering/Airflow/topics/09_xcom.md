## XCom (Cross Communication)
- A way for tasks to share data with each other
- Task A pushes a value → Task B pulls that value
- Stored in the Metadata Database
- Best for small data only (strings, numbers, small dicts)
- Not meant for large data like dataframes

```
# Task A - Push value
def push_function(**context):
    context['ti'].xcom_push(key='my_value', value='Hello')

# Task B - Pull value
def pull_function(**context):
    value = context['ti'].xcom_pull(key='my_value', task_ids='task_a')
    print(value)  # Hello

```

```
# Using TaskFlow API - XCom happens automatically
@task
def task_a():
    return "Hello"        # automatically pushed to XCom

@task
def task_b(value):
    print(value)          # automatically pulled from XCom

value = task_a()
task_b(value)
```