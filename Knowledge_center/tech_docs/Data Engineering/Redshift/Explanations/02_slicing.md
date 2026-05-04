## What is Slicing in Redshift?

### What is it?
- Slicing = how Redshift divides and stores your data across a node
- Each compute node is split into fixed number of slices
- Each slice gets its own chunk of data + its own CPU + its own memory
- Slices work independently and simultaneously

Analogy :

A compute node is a pizza
Slices are pizza slices — each slice is independent
Each person (CPU core) eats their own slice at the same time
Everyone finishes faster than one person eating the whole pizza

---
### What Does a Slice Actually Hold?
- A portion of every table's rows (based on Distribution Style)
- Its own temp space for sorting and hashing
- Processes its portion without depending on other slices

```
Table: Orders (100 rows total, 2 nodes, 2 slices each = 4 slices)

Slice 1 (Node 1) → rows 1-25
Slice 2 (Node 1) → rows 26-50
Slice 3 (Node 2) → rows 51-75
Slice 4 (Node 2) → rows 76-100
```

---
### How Data Gets Into Slices
- When you run COPY command, Redshift automatically distributes rows across slices
- Which rows go to which slice is decided by Distribution Style

| Distribution Style | How rows are assigned to slices |
| :-- | :-- |
| EVEN | Round-robin, rows spread equally |
| KEY | Rows with same key value go to same slice |
| ALL | Full copy of table on every slice |
| AUTO | Redshift decides based on table size |

---
### Key Things to Remember
- Slices are not something you see or touch directly — they are internal
- More slices = more parallelism = faster queries and loads
- Data skew happens when some slices get too many rows vs others → some slices overloaded → slow
- You can check slice distribution using:
```
SELECT slice, COUNT(*) 
FROM stv_blocklist 
GROUP BY slice;
```

---
### Real-World Scenario

You load 1 million orders into Redshift
Cluster has 4 slices total
Redshift splits rows → 250k rows per slice
When you query SUM(sales):

Slice 1 sums its 250k rows
Slice 2 sums its 250k rows
Slice 3 sums its 250k rows
Slice 4 sums its 250k rows
Leader Node adds 4 partial sums → done

All 4 happen at the same time → 4x faster than scanning 1M rows sequentially    

