## DAG Run

- A single execution instance of a DAG
- Every time a DAG executes → one DAG Run is created
- Each DAG Run has its own execution_date
- Can be triggered by schedule, manually or by another DAG
- States → Running / Success / Failed

```
DAG "my_pipeline" scheduled @daily

Jan 1 → DAG Run 1 ✅
Jan 2 → DAG Run 2 ✅
Jan 3 → DAG Run 3 ❌
```