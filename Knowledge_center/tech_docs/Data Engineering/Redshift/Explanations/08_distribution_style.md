## Distribution Styles (AUTO, KEY, EVEN, ALL)

### What is it?
- Controls how Redshift distributes table rows across slices
- Chosen per table when creating it
- Goal: make sure data needed for a query is already on the same slice → avoid moving data across nodes during query execution

Analogy:
- You have 4 warehouses (slices) storing products and orders
- When matching orders to products → if both are in same warehouse → fast
- If product is in warehouse 1 but order is in warehouse 3 → must ship between warehouses → slow
- Distribution Style = strategy for deciding what goes into which warehouse

---
### The Core Problem It Solves — Data Movement
```
SELECT o.order_id, p.product_name
FROM orders o
JOIN products p ON o.product_id = p.product_id;
```

```
If orders and products are on DIFFERENT slices:
Slice 1 has orders → must SEND data to Slice 2 to match products
→ Network shuffle between slices = SLOW (called Broadcast or Redistribute)

If orders and products are on SAME slice (matching product_id):
→ Join happens locally on each slice = FAST (no data movement)
```

---
### 4 Distribution Styles

#### 1. EVEN
Rows distributed round-robin across all slices — purely sequential
No logic — just fills slices evenly one row at a time

```
Row 1  → Slice 1
Row 2  → Slice 2
Row 3  → Slice 3
Row 4  → Slice 4
Row 5  → Slice 1  (starts over)
```

✅ Good for: Tables not used in JOINs, staging tables, equal load distribution
❌ Bad for: Tables frequently joined — matching rows end up on different slices

#### 2. KEY
Rows distributed based on value of a specific column
Same key value always goes to same slice
Matching keys in two tables = co-located on same slice → joins are fast

```
Distribution Key: product_id

product_id = 101 → always Slice 1
product_id = 202 → always Slice 2
product_id = 303 → always Slice 3

orders table (dist key: product_id):
product_id=101 rows → Slice 1

products table (dist key: product_id):
product_id=101 rows → Slice 1

JOIN on product_id → both already on Slice 1 → no data movement ✅
```
✅ Good for: Large fact tables joined frequently on a specific column
❌ Bad for: Low cardinality columns (e.g., gender, status) → causes data skew

#### 3. ALL
Full copy of the entire table on every single node (not slice — node)
Every node has all rows → joins always local → zero data movement
```
Table: products (small, 10k rows)

Node 1: ALL 10k rows
Node 2: ALL 10k rows
Node 3: ALL 10k rows
Node 4: ALL 10k rows
```
✅ Good for: Small dimension/lookup tables joined frequently with large fact tables
❌ Bad for: Large tables — copies multiply storage cost × number of nodes

#### 4. AUTO
Redshift decides the distribution style automatically
Starts as ALL for small tables → switches to EVEN as table grows
Monitors table size and query patterns over time

```
Table starts small (< threshold) → AUTO assigns ALL
Table grows large               → AUTO switches to EVEN
```
✅ Good for: When you're unsure, new tables, tables that grow over time
❌ Bad for: When you know your query patterns — manual KEY is better

---
| Style | How rows distributed | Best For | Watch Out For |
| :-- | :-- | :-- | :-- |
| EVEN | Round-robin, equal spread | Staging, no-join tables | Slow joins |
| KEY | By column value | Large joined fact tables | Data skew on low cardinality |
| ALL | Full copy on every node | Small dimension tables | Storage cost on large tables |
| AUTO | Redshift decides | Default, unsure cases | May not be optimal for complex joins |

---
#### Data Skew — The KEY Distribution Risk

- If distribution key column has few distinct values → some slices get most rows
- Example: distributing by status (only 3 values: active, inactive, pending)

```
If distribution key column has few distinct values → some slices get most rows
Example: distributing by status (only 3 values: active, inactive, pending)
```
Check skew:


```
SELECT slice, COUNT(*)
FROM stv_blocklist
WHERE tbl = (SELECT id FROM stv_tbl_perm WHERE name = 'your_table')
GROUP BY slice
ORDER BY slice;
```

---
### How to Choose Distribution Style


```
Is the table small (< a few million rows)?
    → YES → Use ALL
    → NO  ↓

Is the table frequently JOINed on a specific column?
    → YES → Use KEY on that JOIN column
             (check that column has HIGH cardinality first)
    → NO  ↓

Is the table used standalone (aggregations, no joins)?
    → YES → Use EVEN

Not sure / new table?
    → Use AUTO and let Redshift decide
```

---

### Key Things to Remember
- Distribution style is set at table creation — changing it requires recreating table
- DISTKEY = the column you choose for KEY distribution
Collocated join = both tables distributed on same KEY = no data movement = fast
- ALL copies whole table per node not per slice — storage cost = table size × node count
- Always check for data skew after choosing KEY distribution
- AUTO is default if you don't specify anything

---
### Real-World Use Case
Schema: orders (2 billion rows) joined with products (50k rows) and customers (5M rows)

```
-- orders → KEY on customer_id (large, frequently joined)
CREATE TABLE orders DISTKEY(customer_id) ...

-- products → ALL (small lookup table)
CREATE TABLE products DISTSTYLE ALL ...

-- customers → KEY on customer_id (matches orders distkey)
CREATE TABLE customers DISTKEY(customer_id) ...
```

Result:

- orders JOIN customers → both on same slice by customer_id → no data movement ✅
- orders JOIN products → products fully on every node → always local join ✅
- Query runs significantly faster vs EVEN distribution on all tables