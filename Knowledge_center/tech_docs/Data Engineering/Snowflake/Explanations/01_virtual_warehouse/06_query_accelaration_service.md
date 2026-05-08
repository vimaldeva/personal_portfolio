## Query Acceleration Service (QAS)

### What is it?
- A serverless compute layer that offloads parts of a query that can be parallelized
- Automatically adds extra compute for eligible queries without resizing warehouse
- Available in Enterprise edition and above

Analogy:

Your warehouse = a team of 4 workers
A massive query arrives — too big for just 4 workers
QAS = temporary extra workers hired just for this query
After query done → extra workers gone → billed only for their time


### How it Works

```
Query submitted to Warehouse
        ↓
Snowflake detects query is scan-heavy / eligible for QAS
        ↓
Splits query → part runs on warehouse, part offloaded to QAS serverless nodes
        ↓
Both run in parallel → results merged
        ↓
Faster result than warehouse alone

Without QAS:          With QAS:
Warehouse alone       Warehouse + QAS nodes
→ 5 minutes           → 45 seconds
```

### QAS Eligibility

- Not all queries benefit — QAS helps queries with:

    - Large full table scans
    - Heavy aggregations
    - Unpredictable spikes — one large query among normal workload
- QAS does NOT help:

    - Small queries (already fast)
    - Highly cached queries
    - Queries bottlenecked on joins (not scans)

```
-- Enable QAS on warehouse with scale factor
ALTER WAREHOUSE my_wh SET
    ENABLE_QUERY_ACCELERATION = TRUE
    QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8;
    -- scale factor = max extra compute multiplier
    -- 8 = up to 8x the warehouse size in extra QAS nodes
    -- 0 = unlimited (Snowflake decides)
```


- QAS is billed separately — per-second of serverless compute used
- Scale factor = cost ceiling control — set it to limit unexpected QAS costs
- QAS and multi-cluster warehouses solve different problems:
- Multi-cluster → many concurrent queries (scale out)
- QAS → single large slow query (scale up temporarily)
- Check if query used QAS in Query Profile — look for "Query Acceleration" node
