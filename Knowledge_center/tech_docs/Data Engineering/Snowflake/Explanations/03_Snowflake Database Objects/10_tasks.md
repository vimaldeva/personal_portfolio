## Tasks

### What is it?
- A scheduled or triggered SQL job — runs SQL or stored procedure on a schedule
- Snowflake's built-in scheduler — no external orchestrator needed for simple pipelines

```
-- Warehouse-based task (runs every hour)
CREATE TASK load_orders_task
    WAREHOUSE = 'ETL_WH'
    SCHEDULE = '60 MINUTE'
AS
INSERT INTO orders_final
SELECT * FROM orders_stream
WHERE METADATA$ACTION = 'INSERT';

-- Serverless task (Snowflake manages compute)
CREATE TASK load_orders_task
    SCHEDULE = 'USING CRON 0 * * * * UTC'  -- every hour via CRON
AS
CALL process_orders();

-- Tasks start SUSPENDED — must resume
ALTER TASK load_orders_task RESUME;
ALTER TASK load_orders_task SUSPEND;

-- Manually trigger
EXECUTE TASK load_orders_task;
```

### Task DAGs (Dependencies)

```
-- Root task (runs on schedule)
CREATE TASK root_task
    SCHEDULE = '60 MINUTE'
AS SELECT 1;   -- placeholder

-- Child task (runs after root_task completes)
CREATE TASK child_task_1
    AFTER root_task
AS CALL transform_orders();

-- Another child (runs after root)
CREATE TASK child_task_2
    AFTER root_task
AS CALL transform_customers();

-- Grandchild (runs after both children)
CREATE TASK final_task
    AFTER child_task_1, child_task_2
AS CALL load_final_tables();
```


### Key Things to Remember
- Tasks are SUSPENDED by default — always RESUME after creation
- Only root task has a schedule — child tasks are triggered by parent completion
- Serverless tasks = Snowflake manages compute — no warehouse needed (billed per second)
- Check task history:

```
SELECT * FROM snowflake.account_usage.task_history
ORDER BY scheduled_time DESC;
```