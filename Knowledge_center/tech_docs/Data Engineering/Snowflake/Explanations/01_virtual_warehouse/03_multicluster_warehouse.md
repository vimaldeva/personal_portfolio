## Multi-Cluster Warehouses

### What is it?
- A single warehouse that can spin up multiple identical clusters to handle concurrency
- When too many queries queue up → new cluster automatically starts
- When load drops → extra clusters automatically suspend
Available in Enterprise edition and above

```
Single Cluster Warehouse (M size = 4 nodes):

Peak time: 50 queries submitted
→ 4-8 queries run simultaneously
→ Rest wait in queue  ❌ slow experience

Multi-Cluster Warehouse (M size, max 5 clusters):

Peak time: 50 queries submitted
→ Cluster 1 starts → handles 10 queries
→ Cluster 2 starts → handles 10 queries
→ Cluster 3 starts → handles 10 queries
→ All queries run simultaneously  ✅
```
```
CREATE WAREHOUSE reporting_wh
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 1       -- always keep at least 1 cluster running
    MAX_CLUSTER_COUNT = 5       -- scale up to 5 clusters at peak
    SCALING_POLICY = 'STANDARD' -- or 'ECONOMY'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;
```

### MIN vs MAX Cluster Count

| Setting | Behavior |
| :-- | :-- |
| MIN = 1, MAX = 1 | Single cluster — no auto-scaling (default) |
| MIN = 1, MAX = 5 | Starts with 1, scales to 5 at peak, scales back down |
| MIN = 2, MAX = 5 | Always keeps 2 clusters running — faster response, higher cost |
| MIN = MAX = 3 | Always exactly 3 clusters — fixed concurrency |


### Key Things to Remember
- Each cluster = full copy of the warehouse — same size, same cost per hour
- 3 clusters running = 3x the credits per hour
- Multi-cluster does NOT help with single slow queries — use bigger size for that
- Clusters share same cache — cache reuse across clusters is limited
-       Enterprise edition and above only
