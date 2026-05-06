## Worker
- The component that actually executes the tasks
- Receives tasks from the Executor and runs them
- Can run on the same machine or different machines
- In CeleryExecutor → multiple workers can run in parallel across machines
- More workers = more tasks running simultaneously

```
Scheduler → Executor → Worker 1 → runs task_1
                     → Worker 2 → runs task_2
                     → Worker 3 → runs task_3
```

In AWS MAVAA, it is managed by AWS itself as Fargate containers. You will not manage it