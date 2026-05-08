## Warehouse Scaling Policies (Economy vs Standard)

### What is it?
- Controls how aggressively multi-cluster warehouse spins up / down extra clusters
- Only relevant for multi-cluster warehouses

### Standard Policy (Performance-first)
```
Behavior:
- Spins up new cluster as soon as FIRST query queues
- Shuts down cluster after consecutive checks show it's idle (2-3 min)

Result:
✅ Fastest response — no user waits
❌ More clusters running = higher credit cost
```

### Economy Policy (Cost-first)

```
Behavior:
- Spins up new cluster only when existing cluster is busy for 6+ minutes
- Waits longer before spinning up → queries wait more
- Shuts down idle clusters faster

Result:
✅ Fewer clusters = lower credits
❌ Users may experience queue wait times
```

### Standard vs Economy
| Factor | Standard | Economy |
| :-- | :-- | :-- |
| New cluster trigger | First queued query | Cluster busy for 6+ mins |
| User experience | ✅ No waiting | ❌ Some queue wait |
| Credit consumption | Higher | Lower |
| Best for | BI dashboards, interactive | Batch ETL, cost-sensitive |
| Scale-down speed | Slower (keeps clusters warm) | Faster (shuts down quickly) |

```
-- Set scaling policy
ALTER WAREHOUSE reporting_wh SET SCALING_POLICY = 'STANDARD';
ALTER WAREHOUSE etl_wh SET SCALING_POLICY = 'ECONOMY';
```

### Putting It All Together — Real-World Warehouse Strategy
```
-- BI Team: responsive, multi-cluster, standard policy
CREATE WAREHOUSE bi_warehouse
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 4
    SCALING_POLICY = 'STANDARD'    -- spin up fast
    AUTO_SUSPEND = 600             -- keep warm for 10 mins
    AUTO_RESUME = TRUE;

-- ETL Team: cost-efficient, no concurrency needed
CREATE WAREHOUSE etl_warehouse
    WAREHOUSE_SIZE = 'LARGE'       -- big for heavy transforms
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 1          -- no multi-cluster needed
    AUTO_SUSPEND = 60              -- suspend fast after job
    AUTO_RESUME = TRUE;

-- Dev/Test: minimal cost
CREATE WAREHOUSE dev_warehouse
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;
```






