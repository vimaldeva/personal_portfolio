## DataFrame vs RDD vs Dataset

| Factor | RDD | DataFrame | Dataset |
| :-- | :-- | :-- | :-- |
| Abstraction Level | Low (raw) | High (table-like) | High (typed) |
| Schema | ❌ No schema | ✅ Has schema | ✅ Has schema |
| Type Safety | ❌ No | ❌ No | ✅ Yes (compile-time) |
| Optimization (Catalyst) | ❌ No | ✅ Yes | ✅ Yes |
| Performance | Slower | Fast | Fast |
| Language | Python, Scala, Java | Python, Scala, Java | Scala, Java only |
| Use Case | Fine-grained control | Most common | Typed Scala pipelines |

#### RDD (Resilient Distributed Dataset)
- Lowest level API — collection of objects distributed across cluster
- No schema — just raw Java/Python objects
- You control everything manually
- Use when: custom low-level operations not possible in DataFrame

```
rdd = sc.parallelize([1, 2, 3, 4, 5])
rdd.map(lambda x: x * 2).collect()
# [2, 4, 6, 8, 10]
```
#### DataFrame
- Table with named columns and schema — like a distributed Pandas DataFrame
- Optimized by Catalyst — SQL-like operations
- Most commonly used in modern PySpark

```
df = spark.read.csv("s3://bucket/orders.csv", header=True, inferSchema=True)
df.select("order_id", "revenue").filter("revenue > 1000").show()
```

#### Dataset
- Typed DataFrame — compile-time type safety
- Only available in Scala/Java — in Python, DataFrame IS the Dataset (no distinction)
- In PySpark → you only work with DataFrames

#### Key Things to Remember
- In PySpark → use DataFrame always — RDD only when absolutely needed
- DataFrame → RDD: df.rdd
- RDD → DataFrame: rdd.toDF(["col1", "col2"])
- DataFrame operations go through Catalyst optimizer — RDD operations do NOT
- Avoid converting DataFrame → RDD → back to DataFrame — loses optimization

---
## Array, Map, Struct Column Types

### Struct
- A nested object inside a column — like a row within a row
- Groups multiple fields into one column

```
from pyspark.sql.functions import struct, col

# Create struct column
df = df.withColumn("address", struct(
    col("city"),
    col("state"),
    col("zip")
))

# Access struct fields
df.select("address.city", "address.zip").show()
```

```
Schema:
address: struct
    ├── city: string
    ├── state: string
    └── zip: string
```
### Array
A list of values of the same type inside a single column
```
from pyspark.sql.functions import array, explode, array_contains, array_size

# Create array column
df = df.withColumn("tags", array(lit("electronics"), lit("sale")))

# Explode array → one row per element
df.withColumn("tag", explode(col("tags"))).show()

# Check if value exists
df.filter(array_contains(col("tags"), "sale")).show()

# Get array length
df.withColumn("tag_count", array_size(col("tags"))).show()
```

```
Before explode:               After explode:
order_id | tags               order_id | tag
1        | [electronics, sale] → 1     | electronics
                                1     | sale
```

### Map
A key-value dictionary inside a single column

```
from pyspark.sql.functions import map_keys, map_values, create_map

# Create map column
df = df.withColumn("metadata", create_map(
    lit("source"), lit("web"),
    lit("channel"), lit("organic")
))

# Access map value by key
df.withColumn("source", col("metadata")["source"]).show()

# Get all keys / values
df.withColumn("keys", map_keys(col("metadata"))).show()
df.withColumn("values", map_values(col("metadata"))).show()
```

###
- Key Things to Remember
- Struct = nested object (fixed fields)
- Array = list of same-type values
- Map = key-value pairs (dynamic keys)
- Use explode() to flatten arrays/maps into rows
- Use explode_outer() — same as explode but keeps null rows (explode drops them)
- Dot notation to access struct: col("address.city")
- Bracket notation to access map: col("metadata")["source"]

---

## SQL Functions vs DataFrame Functions

|  | SQL Functions | DataFrame Functions |
| :-- | :-- | :-- |
| How used | Inside spark.sql("...") | Via pyspark.sql.functions import |
| Style | String-based SQL | Python method chaining |
| Performance | Same (both use Catalyst) | Same |
| Readability | Familiar to SQL users | Preferred in code |

### Same Operation — Two Ways

```
from pyspark.sql.functions import upper, col, sum

df.createOrReplaceTempView("orders")

# SQL Function style
spark.sql("""
    SELECT upper(customer_name), SUM(revenue)
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_name
""").show()

# DataFrame Function style
df.filter(col("status") == "completed") \
  .groupBy("customer_name") \
  .agg(sum("revenue")) \
  .withColumn("customer_name", upper(col("customer_name"))) \
  .show()
```

### Key Things to Remember

- Both produce identical execution plans — no performance difference
- Mix them freely — use SQL for complex queries, DF functions in pipeline code
- SQL functions require TempView created first
- DataFrame functions are better for dynamic/programmatic column references
- spark.sql() is great for complex JOINs or CTEs — easier to read

---
## rangeBetween vs rowsBetween

### Context — Window Functions
Both define the frame (boundary) of rows included in a window calculation

```
from pyspark.sql.window import Window
from pyspark.sql.functions import sum, avg

windowSpec = Window.partitionBy("region").orderBy("order_date")
```

### rowsBetween
- Frame based on physical row position relative to current row
- Counts rows regardless of their actual values
```
# Include 2 rows before and 2 rows after current row (by position)
window = Window.partitionBy("region") \
               .orderBy("order_date") \
               .rowsBetween(-2, 2)

df.withColumn("rolling_sum", sum("revenue").over(window)).show()
```
```
Current row position = 0
rowsBetween(-2, 2) includes:
row at -2 (2 rows back)
row at -1 (1 row back)
row at  0 (current)
row at +1 (1 row ahead)
row at +2 (2 rows ahead)
```

### rangeBetween
- Frame based on actual column values relative to current row's value
- Includes all rows where value falls within the range

```
# Include rows where order_date value is within 7 days of current row
window = Window.partitionBy("region") \
               .orderBy("order_date_unix") \
               .rangeBetween(-7, 0)   # 7 units before to current

df.withColumn("rolling_7day_sum", sum("revenue").over(window)).show()
```
```
Current row value = 100
rangeBetween(-20, 0) includes:
all rows where value is between 80 and 100
(regardless of how many rows that is)
```

### rowsBetween vs rangeBetween
|  | rowsBetween | rangeBetween |
| :-- | :-- | :-- |
| Frame boundary | Physical row count | Actual value range |
| Ties handled | Each row counted separately | All tied values included |
| Use case | Rolling N-row window | Rolling value-range window (e.g., 7-day) |

### Special Constants
```
Window.unboundedPreceding   # from very first row
Window.unboundedFollowing   # to very last row
Window.currentRow           # current row

# Running total from start to current row
.rowsBetween(Window.unboundedPreceding, Window.currentRow)

# All rows in partition
.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
```

---
## Subqueries in Spark SQL  

### Types of Subqueries
Scalar Subquery (returns single value)
```
SELECT order_id, revenue,
       (SELECT AVG(revenue) FROM orders) as avg_revenue
FROM orders
```
### IN / NOT IN Subquery
```
SELECT * FROM orders
WHERE customer_id IN (
    SELECT customer_id FROM customers WHERE country = 'US'
)
```
### EXISTS / NOT EXISTS
```
SELECT * FROM orders o
WHERE EXISTS (
    SELECT 1 FROM returns r WHERE r.order_id = o.order_id
)
```
### Correlated Subquery (references outer query)
```
SELECT o.order_id, o.revenue
FROM orders o
WHERE o.revenue > (
    SELECT AVG(revenue) FROM orders
    WHERE region = o.region    -- references outer query's region
)
```

### Key Things to Remember
- Spark supports most subquery types via spark.sql()
- Correlated subqueries can be slow — Spark may not optimize well
- Prefer JOINs over subqueries for better performance in Spark
- Subqueries in DataFrame API = use .join() instead