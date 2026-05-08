## Concurrency and Queuing

### What is it?
- Each warehouse handles limited concurrent queries based on size and available slots
- When all slots are busy → extra queries go into a queue
- Queuing = queries waiting for a slot to open up

### How Concurrency Works
```
Medium warehouse (4 nodes):
Slot capacity: ~8 concurrent queries (varies by query complexity)

10 queries arrive simultaneously:
→ 8 queries run immediately
→ 2 queries wait in queue
→ As a running query finishes → next queued query starts
```

- Snowflake dynamically decides concurrency based on query complexity and memory
- Simple queries = more fit simultaneously
- Heavy queries = fewer fit simultaneously

### Queue Behavior
```
-- Check currently queued and running queries
SELECT query_id, query_text, execution_status, queued_overload_time
FROM snowflake.account_usage.query_history
WHERE warehouse_name = 'MY_WH'
  AND start_time >= DATEADD(hour, -1, CURRENT_TIMESTAMP)
ORDER BY start_time DESC;
```

### Solving Queuing Problems
| Problem | Solution |
| :-- | :-- |
| Few large queries slow | Resize to bigger warehouse |
| Many small concurrent queries queuing | Use multi-cluster warehouse |
| ETL blocking BI queries | Use separate warehouses |
| Occasional huge query spikes | Enable QAS |
| Predictable peak hours | Set MIN_CLUSTER_COUNT > 1 to pre-warm |

### Key Things to Remember
- Queuing is not an error — queries still run, just wait
- Biggest cause of queuing = too many users on same warehouse
- Best solution = separate warehouses per team/workload type
- Monitor queue time in QUERY_HISTORY — QUEUED_OVERLOAD_TIME column
- Queries can also queue due to warehouse being suspended (resume time adds wait)

- What is the normal/default concurrency in snowflake warehouse ?. where can we see it ?
- Default concurrency = based on warehouse size (e.g. Medium = ~10 concurrent queries)