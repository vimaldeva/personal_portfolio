## Leader Node vs. Compute Nodes

## What is it?
- Redshift cluster has two types of nodes working together
- Leader Node — The brain (coordinator)
- Compute Nodes — The muscles (actual workers)

Analogy: Think of a restaurant kitchen.
- Leader Node = Head Chef who takes the order, plans what to cook, assigns tasks
- Compute Nodes = Line Cooks who actually chop, cook, and plate the food

---
### Leader Node
- Entry point for all client connections and SQL queries
- Parses SQL → builds query execution plan → distributes work to compute nodes
- Aggregates results from all compute nodes → sends final result to client
- Does NOT store actual table data
- You are NOT charged separately for the leader node


#### What it does step by step:


```
Client sends SQL Query
        ↓
Leader Node receives it
        ↓
Builds Execution Plan (like a task list)
        ↓
Assigns tasks to Compute Nodes
        ↓
Collects results from all nodes
        ↓
Returns final result to Client
```

---
#### Compute Nodes
- Actually store the data (distributed across nodes)
- Execute the tasks assigned by the leader node in parallel
- Each compute node is split into Slices

##### Node Slices:
- A slice = independent unit of parallel processing within a node
- Each slice gets a portion of the data and processes it simultaneously
- More slices = more parallelism = faster queries

---
### Key Things to Remember
- Only one Leader Node per cluster — always
- Compute Nodes can be scaled up/down (Elastic Resize)
- Leader Node cannot be directly queried or accessed separately
- More compute nodes = more slices = better parallel processing
- If you have 1 node cluster (for dev/test) — leader and compute are on the same node
- Data distribution across slices is controlled by Distribution Style (KEY, EVEN, ALL)

---
### Real-World Use Case
A query runs:

```
SELECT region, SUM(sales) FROM orders GROUP BY region;
```
- Leader Node receives it, plans to scan orders table, assigns scan tasks to all compute nodes
- Each Compute Node scans its slice of data in parallel, calculates partial SUM
- Leader Node collects all partial sums → aggregates → returns final result

Without this split, a 500GB table would be scanned by one machine.
With 4 nodes × 2 slices = 8 parallel workers scanning simultaneously → much faster.