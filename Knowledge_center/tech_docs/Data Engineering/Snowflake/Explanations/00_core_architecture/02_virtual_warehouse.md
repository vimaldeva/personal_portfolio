## Virtual Warehouses

### What is it?
- A cluster of compute resources (CPU + memory + local SSD) that executes queries
- Like renting a specific-sized engine to run your SQL
Starts, runs, and suspends independently

Analogy:

Snowflake storage = a shared library of books
Virtual Warehouse = a reading room you rent
Multiple teams rent different reading rooms — all reading same books simultaneously

### Warehouse Sizes & Credits
| Size | Servers | Credits/Hour | Best For |
| :-- | :-- | :-- | :-- |
| X-Small (XS) | 1 | 1 | Dev, small queries |
| Small (S) | 2 | 2 | Light workloads |
| Medium (M) | 4 | 4 | Regular BI queries |
| Large (L) | 8 | 8 | Heavy analytics |
| X-Large (XL) | 16 | 16 | Complex transforms |
| 2X-Large | 32 | 32 | Large ETL |
| 3X-Large | 64 | 64 | Very large workloads |
| 4X-Large | 128 | 128 | Massive workloads |

- Credits double with each size up
- Bigger ≠ always faster — depends on query complexity and data volume

---
### Auto-Suspend & Auto-Resume

```
CREATE WAREHOUSE my_warehouse
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300        -- suspend after 5 mins of inactivity (seconds)
    AUTO_RESUME = TRUE;       -- auto-starts when query submitted
```

- Auto-suspend = cost saving — no credits when idle
- Auto-resume = transparent to users — warehouse starts automatically
- Minimum billing = 60 seconds per start


### Multi-Cluster Warehouses
- Single warehouse can have multiple clusters running in parallel
- Handles concurrency spikes — extra clusters spin up automatically
- Available in Enterprise edition and above


```
Normal load:    Cluster 1 handles all queries
Peak load:      Cluster 1 + Cluster 2 + Cluster 3 spin up automatically
Load drops:     Extra clusters suspended automatically
```
```
CREATE WAREHOUSE my_warehouse
    WAREHOUSE_SIZE = 'LARGE'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 5        -- up to 5 clusters during peak
    SCALING_POLICY = 'STANDARD'; -- Economy = saves credits, Standard = performance
```

### Key Things to Remember
- Each warehouse = completely isolated compute — no sharing between warehouses
- Suspend warehouse immediately if not needed:

```
ALTER WAREHOUSE my_warehouse SUSPEND;
ALTER WAREHOUSE my_warehouse RESUME;
```

- Warehouse cache is lost on suspend — first queries - after resume hit storage
- Bigger warehouse = faster complex queries but more credits per hour
- Use separate warehouses for ETL vs BI vs Data Science — true isolation
- Query queuing happens when all slots in warehouse are busy