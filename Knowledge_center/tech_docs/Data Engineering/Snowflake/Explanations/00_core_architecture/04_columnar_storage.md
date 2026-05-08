## Columnar Storage

### What is it?
- Snowflake stores data by column, not by row within each micro-partition
- Same concept as Redshift columnar storage — only relevant columns read during query

Analogy:

Row storage = spreadsheet saved row by row — to find all salaries, read every row
Columnar = spreadsheet saved column by column — jump straight to salary column

---
### Row vs Columnar (Quick Visual)

```
Table: employees (4 columns, 3 rows)

Row Storage (traditional):
Block 1: [John, 30, NYC, 80000] [Jane, 25, LA, 90000] [Bob, 35, SF, 70000]
→ SUM(salary) = must read ALL columns to get salary ❌

Columnar Storage (Snowflake):
Block - name:   [John, Jane, Bob]
Block - age:    [30, 25, 35]
Block - city:   [NYC, LA, SF]
Block - salary: [80000, 90000, 70000]
→ SUM(salary) = read ONLY salary block ✅
```

### Benefits in Snowflake

```
| Benefit | How |
| :-- | :-- |
| I/O reduction | Only queried columns read from storage |
| Better compression | Same data type per column → compresses well |
| Faster aggregations | SUM/AVG/COUNT on one column block |
| Metadata richness | MIN/MAX/COUNT per column stored in micro-partition metadata |
```

### Key Things to Remember
- SELECT * = reads all column blocks — avoid on large tables
- Snowflake auto-selects compression per column based on data type and cardinality
- Works hand-in-hand with micro-partitions — columnar within each partition
- Compression ratio can be 3x-10x depending on column data

---



