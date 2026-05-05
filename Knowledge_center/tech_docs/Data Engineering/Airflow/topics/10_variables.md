## Variable
- A way to store global key-value pairs in Airflow
- Stored in the Metadata Database
- Accessible from any DAG or task
- Used to store config values, flags, environment names etc.
- Can be managed from UI or CLI

```
from airflow.models import Variable

# Set a variable
Variable.set("environment", "production")

# Get a variable
env = Variable.get("environment")
print(env)  # production

# Get a JSON variable
config = Variable.get("db_config", deserialize_json=True)
print(config["host"])
```

```
# From CLI
airflow variables set environment production
airflow variables get environment

```


Quick Difference - XCom vs Variable


|  | XCom | Variable |
| :-- | :-- | :-- |
| Scope | Between tasks in a DAG | Global across all DAGs |
| Purpose | Pass data between tasks | Store config/settings |
| Lifetime | Tied to a DAG Run | Permanent until deleted |
| Best for | Task outputs | Environment configs, flags |


