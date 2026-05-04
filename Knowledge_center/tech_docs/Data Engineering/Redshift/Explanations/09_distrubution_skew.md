## Distribution Skew

- Happens when data is unevenly distributed across slices
- Some slices get too many rows, others get very few
- The query speed = speed of the slowest slice — overloaded slices become bottlenecks

Analogy:

4 cashiers at a supermarket (slices)
Cashier 1 has 50 customers in line
Cashiers 2, 3, 4 have 2 customers each
Everyone waits until Cashier 1 is done — other cashiers sitting idle
Total time = Cashier 1's time, not average time

---
### Why it Happens

- Almost always caused by a bad choice of DISTKEY
- Low cardinality column used as DISTKEY → few distinct values → rows pile up on few slices

```
DISTKEY = payment_status (only 3 values)

Slice 1 → payment_status = 'completed'  → 95% of rows 🔴
Slice 2 → payment_status = 'pending'    → 4%  of rows
Slice 3 → payment_status = 'failed'     → 1%  of rows
Slice 4 →                               → 0%  of rows (empty)
```

---
### Two Types of Skew

#### 1. Data Skew (Storage Skew)
- Uneven number of rows stored across slices
- Caused by bad DISTKEY choice
- Affects both storage and query performance

#### 2. Compute Skew (Processing Skew)
- Uneven amount of work done during query execution
- Happens even with EVEN distribution if query has:
- Heavy GROUP BY on low cardinality column
- Skewed JOIN where one key value has millions of matches


--- 
### How to Detect Skew
#### Check Storage Skew (rows per slice):

```
-- See how many rows each slice holds for a table
SELECT slice, num_values as rows
FROM svv_diskusage
WHERE name = 'your_table_name'
ORDER BY slice;
```

#### Check Table Skew Ratio:
``` SELECT
  trim(name) as table_name,
  max(num_values) as max_rows_on_slice,
  min(num_values) as min_rows_on_slice,
  max(num_values) - min(num_values) as skew_difference
FROM svv_diskusage
WHERE name = 'your_table_name'
GROUP BY name;
```

#### Check Query-Level Skew (via STL_QUERY_METRICS):
```
SELECT query, slice, rows, cpu_time
FROM stl_query_metrics
WHERE query = <your_query_id>
ORDER BY slice;
-- If one slice shows massively higher rows/cpu_time = compute skew
```

---
### How to Fix Distribution Skew
#### Fix 1: Choose a Better DISTKEY (High Cardinality Column)
sql

```
-- BAD: Low cardinality → skew
CREATE TABLE orders DISTKEY(payment_status) ...

-- GOOD: High cardinality → even spread
CREATE TABLE orders DISTKEY(customer_id) ...

```

#### Fix 2: Switch to EVEN if no good DISTKEY exists

```
-- When no column is a good distribution key
CREATE TABLE orders DISTSTYLE EVEN ...
-- Trades join performance for even distribution

```

#### Fix 3: Use EVEN for the skewed table + ALL for small joined table

```

CREATE TABLE orders DISTSTYLE EVEN ...        -- large skewed table
CREATE TABLE products DISTSTYLE ALL ...       -- small lookup table
-- products copied to every node → joins still local

```

#### Fix 4: Recreate the Table with Better Distribution


```
-- Redshift doesn't allow ALTER DISTKEY directly
-- Must recreate:
CREATE TABLE orders_new DISTKEY(customer_id) AS
SELECT * FROM orders;

ALTER TABLE orders RENAME TO orders_old;
ALTER TABLE orders_new RENAME TO orders;
DROP TABLE orders_old;

```

| Column | Good DISTKEY? | Why |
| :-- | :-- | :-- |
| customer_id (millions of users) | ✅ Yes | High cardinality, even spread |
| order_id (unique per row) | ✅ Yes | Maximum cardinality |
| payment_status (3 values) | ❌ No | Low cardinality, causes skew |
| country (few countries dominate) | ❌ No | Uneven value frequency |
| product_category (10 categories) | ❌ No | Too few distinct values |

---
### Key Things to Remember
- Skew = worst slice determines total query time — other slices sit idle
- Always pick high cardinality + frequently joined column as DISTKEY
- High cardinality alone isn't enough — values must also be evenly frequent
- EVEN distribution never causes storage skew but can cause compute skew
- Skew is invisible until you query — always check after table creation
- Changing DISTKEY = must recreate the table — plan carefully upfront

---
