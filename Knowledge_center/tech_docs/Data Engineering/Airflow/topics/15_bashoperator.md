## BashOperator
- Runs a Bash command or shell script inside a task

```
from airflow.operators.bash import BashOperator

# Simple command
task = BashOperator(
    task_id="print_hello",
    bash_command="echo Hello Airflow"
)

# Run a python script
task = BashOperator(
    task_id="run_script",
    bash_command="python /scripts/process_data.py --date {{ ds }}"
)

# Multiple commands
task = BashOperator(
    task_id="multiple_commands",
    bash_command="""
        echo "Starting" &&
        cd /data &&
        python transform.py &&
        echo "Done"
    """
)

# With environment variables
task = BashOperator(
    task_id="with_env",
    bash_command="echo $MY_VAR",
    env={"MY_VAR": "hello", "ENV": "production"}
)
```

#### Common Use Cases

- Run shell scripts
- Run Python scripts via CLI
- File operations (move, copy, delete)
- Trigger CLI tools (dbt, spark-submit)