## Dag Runs

A Dag Run is an object representing an instantiation of the Dag in time. Any time the Dag is executed, a Dag Run is created and all tasks inside it are executed. The status of the Dag Run depends on the tasks states. Each Dag Run is run separately from one another, meaning that you can have many runs of a Dag at the same time.


There are two possible terminal states for the Dag Run:

- success if all of the leaf nodes states are either success or skipped,

- failed if any of the leaf nodes state is either failed or upstream_failed.

### Backfill

You may want to run the Dag for a specified historical period. For example, a Dag is created with start_date 2024-11-21, but another user requires the output data from a month prior, i.e. 2024-10-21. This process is known as Backfill.

This can be done through either the UI or CLI.

From the Dag Details page, click Trigger and select Backfill to open the backfill form. Set the date range, reprocess behavior, max active runs, optional backwards ordering, and Advanced Config.
![Backfill form](backfill.png)

```
airflow backfill create --dag-id DAG_ID \
    --start-date START_DATE \
    --end-date END_DATE \
    --reprocessing-behavior failed \
    --max-active-runs 3 \
    --run-backwards \
    --dag-run-conf '{"my": "param"}'
```
    