## Query Plan / Explain Plan

### What is it?
- A breakdown of how Redshift executes your query — step by step
- Shows what operations happen, in what order, and at what cost
- Used to identify why a query is slow and how to optimize it

Analogy:

You ask for directions from A to B
EXPLAIN = GPS showing you the full route with each turn before you drive
Helps you spot if the route is inefficient before wasting time

```
-- Shows estimated plan (query does NOT actually run)
EXPLAIN SELECT * FROM orders WHERE order_date = '2024-01-15';

-- Shows actual execution plan with real metrics (query RUNS)
EXPLAIN ANALYZE SELECT * FROM orders WHERE order_date = '2024-01-15';
```

#### Reading the Output


```
QUERY PLAN
------------------------------------------
XN Aggregate  (cost=1000.00..1000.01)        ← Step 4: final aggregation on Leader
  -> XN Seq Scan on orders                   ← Step 1: full table scan
       Filter: (order_date = '2024-01-15')   ← Step 2: filter applied
  -> XN Hash Join                            ← Step 3: join operation
       Hash Cond: (o.customer_id = c.id)
```

- Read from bottom to top — bottom is what happens first
- XN prefix = operation runs on compute nodes
- cost=X..Y = estimated cost units (relative, not seconds)

---
### Key Operations to Recognize

| Operation | What it Means |
| :-- | :-- |
| Seq Scan | Full table scan — reads all blocks |
| Hash Join | Join using hash table — good for large joins |
| Nested Loop | Row by row join — very slow, avoid |
| Broadcast | Entire table sent to all nodes — data movement |
| Redistribute | Rows shuffled across slices — data movement |
| DS_BCAST_INNER | Inner table broadcast — signals missing colocation |
| DS_DIST_BOTH | Both tables redistributed — worst case, heavy data movement |
| DS_DIST_NONE | No redistribution needed — best case ✅ |

### Red Flags in Explain Plan


```
❌ DS_BCAST_INNER   → table broadcast across all nodes (check distribution)
❌ DS_DIST_BOTH     → both sides of join redistributed (bad DISTKEY choice)
❌ Nested Loop      → extremely slow join, usually a cartesian product
❌ Seq Scan on huge table with no filter → missing Sort Key
❌ Very high cost number on one step → bottleneck found here
```

---
### Key Things to Remember
- EXPLAIN = estimated plan, query doesn't run — safe to use anytime
- EXPLAIN ANALYZE = actual plan with real numbers, query actually runs
- Plans execute bottom to top — always read from bottom
- DS_DIST_NONE = no data movement = ideal
- High cost on a Seq Scan → check if Sort Key + Zone Maps can help
- Data movement steps (Broadcast, Redistribute) = biggest performance killers → fix with Distribution Style