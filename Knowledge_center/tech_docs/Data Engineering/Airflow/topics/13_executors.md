## Executor
- Defines how and where tasks get executed
- Scheduler decides when to run → Executor decides how to run
- You configure Executor in airflow.cfg

```
Scheduler → hands over task → Executor → runs on Worker
```

Types of Executors


| Executor | Best For |
| :-- | :-- |
| SequentialExecutor | Development only, one task at a time |
| LocalExecutor | Single machine, runs tasks in parallel |
| CeleryExecutor | Multiple machines, distributed execution |
| KubernetesExecutor | Each task runs in its own K8s pod |

```
# airflow.cfg
executor = CeleryExecutor

# CeleryExecutor needs a broker
broker_url = redis://localhost:6379/0
```

CeleryExecutor Architecture

```
Scheduler
    ↓
Celery Broker (Redis/RabbitMQ)
    ↓
Worker 1 | Worker 2 | Worker 3
```


In AWS MAVAA, it is managed by AWS itself . You will not manage it