## Micro-partitions

### What is it?
- Snowflake automatically divides table data into small immutable chunks called micro-partitions
- Each micro-partition = 50-500MB of uncompressed data (much smaller when compressed)
- Stored in columnar format — each column stored separately within partition
- Automatically created and managed by Snowflake — you don't control partitioning

Analogy:

Your table data = a large book
Micro-partitions = chapters of the book
Each chapter is stored with an index (metadata) saying what's inside
Finding info = check index first → go directly to right chapter → skip everything else

### Structure of a Micro-partition

```
Micro-partition File:
┌────────────────────────────────┐
│ Column 1: order_date           │  [2024-01-01 ... 2024-01-10]
│ Column 2: region               │  [EAST, WEST, EAST, NORTH...]
│ Column 3: revenue              │  [100, 250, 340, 180...]
│ Column 4: customer_id          │  [101, 203, 105, 301...]
├────────────────────────────────┤
│ Metadata (stored separately):  │
│  - Row count: 50,000           │
│  - MIN/MAX per column          │
│  - NULL count                  │
│  - Distinct values count       │
└────────────────────────────────┘
```

---

### How Partition Pruning Works

```
SELECT SUM(revenue)
FROM orders
WHERE order_date = '2024-06-15'
  AND region = 'EAST';
```

```
Snowflake checks micro-partition metadata FIRST (no data scan):

Partition 1: dates Jan1-Jan31, regions [EAST,WEST]  → SKIP (no June dates)
Partition 2: dates Jun1-Jun15, regions [EAST,NORTH] → SCAN ✅
Partition 3: dates Jun16-Jun30, regions [WEST,SOUTH] → SKIP (no June 15)
Partition 4: dates Jul1-Jul31, regions [EAST,WEST]  → SKIP (no June dates)

Only Partition 2 scanned → massive I/O savings
```

---

### Clustering Keys
- By default Snowflake partitions data in insertion order
- If queries filter on a column that's scattered across all partitions → pruning is poor
- Clustering Key = tell Snowflake to organize micro-partitions around specific column(s)

```
-- Add clustering key to large table
ALTER TABLE orders CLUSTER BY (order_date, region);
```

```
Without clustering (insertion order):
Partition 1: dates mixed [Jan, Jun, Mar, Nov] → can't prune by date ❌

With clustering on order_date:
Partition 1: dates [Jan 1-10] → easily pruned ✅
Partition 2: dates [Jan 11-20] → easily pruned ✅
```

---
### Clustering Depth
- Measures how well-organized the micro-partitions are for a given clustering key
- Lower depth = better clustering = better pruning = faster queries
Check via:
```
SELECT SYSTEM$CLUSTERING_INFORMATION('orders', '(order_date)');
```

### Key Things to Remember
- Micro-partitions are automatically created — you don't define partition size
- Each micro-partition has rich metadata — Snowflake uses it for pruning without scanning data
- Micro-partitions are immutable — updates/deletes create new partitions (old ones marked for deletion)
- Clustering Keys only needed for very large tables (hundreds of GB+)
- Adding a Clustering Key = ongoing cost (automatic reclustering runs in background)
- Check partition pruning in Query Profile — look at "Partitions Scanned vs Total"

```
Query submitted
       ↓
Cloud Services Layer parses + optimizes query (Layer 3)
       ↓
Checks micro-partition METADATA → identifies which partitions to scan
       ↓
Virtual Warehouse activated (Layer 2)
       ↓
Checks local SSD cache first → if data cached → no storage read needed
       ↓
Fetches only relevant micro-partitions from Storage Layer (Layer 1)
       ↓
Processes columnar data in parallel across warehouse nodes
       ↓
Result returned → cached in Result Cache for future identical queries
```