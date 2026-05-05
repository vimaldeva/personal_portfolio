## Task
- A single unit of work inside a DAG
- Defined using Operators
- Tasks are connected to define the order of execution
python

```
task_1 >> task_2 >> task_3
# task_1 runs first, then task_2, then task_3

```