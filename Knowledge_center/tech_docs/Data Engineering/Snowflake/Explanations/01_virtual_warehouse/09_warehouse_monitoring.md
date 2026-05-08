## Warehouse Monitoring

### Where to Monitor
1. Snowflake Web UI (Snowsight)
    - Admin → Warehouses → visual credit usage per warehouse
    - Activity → Query History → see all queries, duration, credits, status
    - Admin → Cost Management → overall credit spend

2. ACCOUNT_USAGE Schema (Historical — up to 1 year)
```
-- Credit consumption per warehouse (last 30 days)
SELECT warehouse_name,
       SUM(credits_used) as total_credits,
       SUM(credits_used_compute) as compute_credits,
       SUM(credits_used_cloud_services) as cloud_service_credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP)
GROUP BY warehouse_name
ORDER BY total_credits DESC;
```

```
-- Long running queries on a warehouse
SELECT query_id, query_text, warehouse_name,
       total_elapsed_time/1000 as duration_seconds,
       credits_used_cloud_services
FROM snowflake.account_usage.query_history
WHERE warehouse_name = 'ANALYTICS_WH'
  AND total_elapsed_time > 60000   -- queries > 60 seconds
  AND start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP)
ORDER BY total_elapsed_time DESC;
```

```
-- Queued queries (high overload time = queuing problem)
SELECT warehouse_name,
       AVG(queued_overload_time)/1000 as avg_queue_seconds,
       COUNT(*) as query_count
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP)
GROUP BY warehouse_name
ORDER BY avg_queue_seconds DESC;
```

3. INFORMATION_SCHEMA (Real-time — short retention)

```
-- Currently running queries RIGHT NOW
SELECT query_id, query_text, execution_status,
       total_elapsed_time/1000 as seconds_running
FROM table(information_schema.query_history_by_warehouse(
    warehouse_name => 'MY_WH',
    result_limit => 20
))
ORDER BY start_time DESC;
```

### Key Metrics to Monitor
| Metric | What it Tells You | Where |
| :-- | :-- | :-- |
| credits_used | Cost per warehouse | WAREHOUSE_METERING_HISTORY |
| total_elapsed_time | Query duration | QUERY_HISTORY |
| queued_overload_time | Time spent queuing | QUERY_HISTORY |
| bytes_scanned | Data scanned per query | QUERY_HISTORY |
| partitions_scanned vs total | Pruning effectiveness | QUERY_HISTORY |
| bytes_spilled_to_local_storage | Warehouse too small | QUERY_HISTORY |
| bytes_spilled_to_remote_storage | Severely undersized | QUERY_HISTORY |

### Spilling — Critical Warning Sign
```
-- Find queries spilling to disk (warehouse too small)
SELECT query_id, query_text, warehouse_name,
       bytes_spilled_to_local_storage,
       bytes_spilled_to_remote_storage
FROM snowflake.account_usage.query_history
WHERE (bytes_spilled_to_local_storage > 0
   OR bytes_spilled_to_remote_storage > 0)
  AND start_time >= DATEADD(day, -7, CURRENT_TIMESTAMP)
ORDER BY bytes_spilled_to_remote_storage DESC;
```

```
bytes_spilled_to_local_storage  → moderate spill, upgrade warehouse size
bytes_spilled_to_remote_storage → severe spill, definitely upgrade size
```
### Real-World Monitoring Routine


```
Daily:
→ Check top 10 credit-consuming warehouses
→ Check if any warehouse running 24/7 (forgot to suspend)

Weekly:
→ Check queries with high queued_overload_time → resize or multi-cluster
→ Check queries spilling to disk → resize warehouse
→ Check bytes_scanned outliers → missing clustering or bad query

Monthly:
→ Compare credit budget vs actual (Resource Monitor)
→ Review warehouses with low utilization → downsize or merge
→ Review Time Travel storage cost → adjust retention if needed
```