## Columnar Storage in Redshift

### What is it?
- A method of storing table data by column instead of by row
- Traditional databases store one full row together on disk
- Redshift stores all values of one column together on disk

Analogy:

Row storage = Filing cabinet — each drawer has one person's full file (name, age, salary, address together)

Columnar storage = Spreadsheet sorted by column — all names in one place, all salaries in one place

If you only need salaries → open only the salary drawer, ignore everything else

---
### Why it Matters for Analytics
- Analytical queries rarely need all columns
- ey typically do SUM, AVG, COUNT, GROUP BY on 2-3 columns out of 50+
- Columnar storage means only relevant columns are read from disk → massive I/O savings

---
### Extra Benefits of Columnar Storage
1. Better Compression
- Same column = same data type = similar values stored together
- Similar values compress much better than mixed row data

```
Salary column: [50000, 50000, 51000, 50000, 52000]
→ Very repetitive → compresses extremely well (up to 10x)

Mixed row: [John, 25, NYC, 50000]
→ Different types, different values → compresses poorly
```

2. Zone Maps
- Redshift automatically tracks MIN and MAX value of each block per column
- Before scanning, checks zone map → skips blocks that can't have matching values

```
Query: WHERE salary > 100000

Zone Map Block 1: MIN=40000, MAX=60000 → SKIP (no values > 100000)
Zone Map Block 2: MIN=90000, MAX=120000 → SCAN (might have matches)
```

---
### When Columnar is Fast vs Slow

| Scenario | Performance |
| :-- | :-- |
| SELECT col1, SUM(col2) GROUP BY col1 | ✅ Very Fast |
| Scanning specific columns with filters | ✅ Very Fast |
| SELECT * on wide tables | ⚠️ Slower (reads all columns) |
| Frequent single-row lookups by ID | ❌ Not ideal (Row DB better) |
| INSERT/UPDATE single rows frequently | ❌ Not ideal (OLTP DB better) |

---

### Key Things to Remember
- Redshift columnar storage is why SELECT * is bad practice — always select only needed columns
- Column data is stored in 1MB immutable blocks on disk
- Each column block is independently compressed using encoding (AZ64, ZSTD, LZO etc.)
- Columnar = great for OLAP (analytics), bad for OLTP (transactions)
- Works hand-in-hand with Sort Keys (skip blocks) and Compression (reduce I/O)
- Redshift auto-assigns compression encoding per column if you use COPY command

