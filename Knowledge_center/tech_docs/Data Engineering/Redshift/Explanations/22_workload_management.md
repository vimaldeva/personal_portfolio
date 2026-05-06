## Workload Management (WLM)

## What is it?
- Controls how queries are prioritized, queued, and allocated memory/concurrency in Redshift
- Prevents one heavy query from consuming all resources and blocking others
- Think of it as a traffic management system for queries

Analogy:

Airport with one runway (compute resources)
WLM = air traffic controller deciding which planes land first
VIP flights (critical queries) get priority over cargo flights (batch jobs)

### The Problem WLM Solves


```
Without WLM:
Heavy BI report → consumes all memory → 20 other queries stuck waiting

With WLM:
BI reports     → Queue 1 (high priority, 40% memory)
ETL jobs       → Queue 2 (medium priority, 40% memory)
Ad-hoc queries → Queue 3 (low priority, 20% memory)
All run simultaneously without blocking each other
```
---
### Two Modes

#### Automatic WLM (Default — Recommended)
- Redshift automatically manages memory and concurrency
- Adjusts dynamically based on query complexity and cluster load
- You just set Query Priorities — Redshift handles the rest

```
-- Set query priority for a session
SET query_group TO 'high';
SET wlm_query_slot_count TO 4;  -- give this query more slots
```
Priority Levels (Automatic WLM):

| Priority | Use For |
| :-- | :-- |
| CRITICAL | Most urgent queries |
| HIGHEST | Important dashboards |
| HIGH | BI reports |
| NORMAL | Default |
| LOW | Batch/ETL jobs |
| LOWEST | Background jobs |

#### Manual WLM
- You manually define queues with fixed memory % and concurrency slots
- Each queue handles specific user groups or query groups
- Requires cluster restart to apply changes

```
WLM Configuration (JSON):
[
  {
    "name": "BI_queue",
    "memory_percent_to_use": 40,
    "query_concurrency": 5,
    "user_group": ["bi_users"]
  },
  {
    "name": "ETL_queue",
    "memory_percent_to_use": 40,
    "query_concurrency": 3,
    "user_group": ["etl_users"]
  },
  {
    "name": "default_queue",
    "memory_percent_to_use": 20,
    "query_concurrency": 5
  }
]
```

#### Automatic vs Manual WLM

| Factor | Automatic | Manual |
| :-- | :-- | :-- |
| Memory management | Dynamic | Fixed % per queue |
| Concurrency | Auto-scales | Fixed slots per queue |
| Setup complexity | Simple | Complex |
| Flexibility | High | Low |
| Restart needed for changes | ❌ No | ✅ Yes |
| AWS Recommendation | ✅ Preferred | ⚠️ Legacy |

---
### Key Things to Remember
- Automatic WLM is recommended — Manual WLM is considered legacy
- Each manual queue has slots — slot = memory + CPU unit for one query
- More slots = more concurrency but less memory per query
- SET wlm_query_slot_count = give a single query more memory (fewer concurrent queries allowed)
- Queries not matching any queue → go to default queue
Check queue wait times:

```
SELECT * FROM stv_wlm_query_state;        -- current queue state
SELECT * FROM stl_wlm_query               -- historical queue data
ORDER BY queue_start_time DESC;
``` 

---

### Real-World Use Case
Redshift cluster shared by 3 teams:

- Executives running critical dashboards → need instant results
- Data Analysts running BI reports → medium priority
- ETL pipelines running nightly → can wait

With Automatic WLM + priorities:

```
-- Executive session
SET priority TO CRITICAL;

-- ETL session
SET priority TO LOW;
``` 

- Executives always get resources first
- ETL runs in background without blocking dashboards
- No manual queue configuration needed ✅