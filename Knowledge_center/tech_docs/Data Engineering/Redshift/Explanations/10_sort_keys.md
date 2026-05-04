### Sort Keys (Compound vs. Interleaved)

- Defines the order in which data is physically stored on disk within each slice
- When data is sorted → Zone Maps become effective → blocks get skipped → faster queries
- Chosen per table, on one or more columns

Analogy:

Unsorted data = Books randomly thrown on shelves
Finding "Harry Potter" = check every book

Sorted data = Books sorted alphabetically
Finding "Harry Potter" = go straight to H section, skip everything else
Zone Maps = the library index telling you exactly which shelf to check

---
### Why Sort Keys Matter


```
Table: orders (sorted by order_date)

Block 1 → dates: Jan 1 to Jan 10   Zone Map: MIN=Jan1,  MAX=Jan10
Block 2 → dates: Jan 11 to Jan 20  Zone Map: MIN=Jan11, MAX=Jan20
Block 3 → dates: Jan 21 to Jan 31  Zone Map: MIN=Jan21, MAX=Jan31
Block 4 → dates: Feb 1  to Feb 10  Zone Map: MIN=Feb1,  MAX=Feb10

Query: WHERE order_date = 'Jan 25'
→ Blocks 1, 2, 4 SKIPPED instantly via Zone Maps
→ Only Block 3 scanned ✅
```
Without Sort Key → dates scattered → Zone Map ranges overlap → all blocks scanned


---
### Two Types of Sort Keys
#### 1. Compound Sort Key
- Sorts data by columns in the exact order specified — like a phone book (last name → first name)
- First column is the primary sort, second is sort within first, and so on
- Zone Maps work best on leading column(s)

```
CREATE TABLE orders (
    order_date DATE,
    region VARCHAR,
    product_id INT,
    revenue DECIMAL
) COMPOUND SORTKEY(order_date, region);
```
```
CREATE TABLE orders (
    order_date DATE,
    region VARCHAR,
    product_id INT,
    revenue DECIMAL
) COMPOUND SORTKEY(order_date, region);
```
Zone Map effectiveness:

```
Query: WHERE order_date = '2024-01-15'
→ Zone Maps on order_date → skip most blocks ✅ (very effective)

Query: WHERE region = 'EAST'
→ Region is 2nd column → mixed across all blocks → Zone Maps barely help ❌

Query: WHERE order_date = '2024-01-15' AND region = 'EAST'
→ Narrows by date first → then filters region ✅ (good)

```


✅ Best when: Queries consistently filter on the first column or first few columns
❌ Weak when: Queries skip the leading column and filter on only later columns


#### 2. Interleaved Sort Key
- Gives equal weight to all sort key columns
- No "leading column" concept — any column can be the primary filter
- Data is sorted using a space-filling curve across all columns equally

```
2. Interleaved Sort Key
Gives equal weight to all sort key columns
No "leading column" concept — any column can be the primary filter
Data is sorted using a space-filling curve across all columns equally
```
Zone Map effectiveness:

```
Query: WHERE order_date = '2024-01-15'        → ✅ effective
Query: WHERE region = 'EAST'                  → ✅ effective
Query: WHERE product_id = 101                 → ✅ effective
Query: WHERE region = 'EAST' AND product_id=101 → ✅ effective
```
✅ Best when: Queries filter on different columns unpredictably
❌ Weak when:

- Table has frequent inserts/updates → interleaved becomes unsorted quickly
- VACUUM REINDEX is expensive on large tables (much slower than compound VACUUM)

---
### Compound vs Interleaved — Direct Comparison

| Factor | Compound | Interleaved |
| :-- | :-- | :-- |
| Sort priority | First column dominates | All columns equal |
| Best query pattern | Filters on leading column(s) | Filters on any column unpredictably |
| VACUUM cost | Fast (VACUUM SORT ONLY) | Expensive (VACUUM REINDEX) |
| Insert performance | Good | Degrades faster over time |
| Typical use case | Time-series, date-range queries | Ad-hoc, multi-dimensional queries |
| AWS recommendation | ✅ Preferred | ⚠️ Use carefully |

Note: AWS now recommends Compound over Interleaved in most cases
Interleaved maintenance cost often outweighs its benefits

---
#### AUTO Sort Key
Redshift can automatically choose sort key based on query patterns
Uses SORTKEY AUTO or just don't specify any sort key
Good for new tables where query patterns are unknown

```
CREATE TABLE orders SORTKEY AUTO ...
-- Redshift monitors queries and picks best sort key over time
```

---
### VACUUM — Keeping Sort Keys Effective

New data inserted goes to unsorted region at bottom of table
Over time → large unsorted region → Zone Maps lose effectiveness → queries slow down
VACUUM re-sorts the data and reclaims space from ghost rows
```
New data inserted goes to unsorted region at bottom of table
Over time → large unsorted region → Zone Maps lose effectiveness → queries slow down
VACUUM re-sorts the data and reclaims space from ghost rows
```

---
### How to Choose Sort Key Columns

```
What column appears most in WHERE clauses?
    → Make it SORT KEY column 1

Do queries always filter on same column(s)?
    → Use COMPOUND SORTKEY(col1, col2)

Do queries filter on different columns unpredictably?
    → Consider INTERLEAVED (but weigh VACUUM cost)

Is this a time-series table (logs, events, transactions)?
    → COMPOUND SORTKEY(timestamp_column) — almost always best choice

Not sure?
    → Use AUTO or COMPOUND on most common filter column
    
```

---
### Sort Key + Distribution Key Together

Often the same column is both DISTKEY and SORTKEY
Very common pattern for fact tables


```
CREATE TABLE orders (
    customer_id BIGINT,
    order_date  DATE,
    revenue     DECIMAL
)
DISTKEY(customer_id)                        -- distribute by customer
COMPOUND SORTKEY(customer_id, order_date);  -- sort by customer then date

-- Queries joining on customer_id + filtering by date = very fast
```


---
### Key Things to Remember

- Sort Key = physical sort order on disk, not a traditional index
- Only one Sort Key per table (can be multi-column)
- Sort Key effectiveness depends on how sorted the data actually is — VACUUM maintains it
- Compound is better default choice — simpler, cheaper to maintain
- Interleaved VACUUM REINDEX = very expensive on large tables
- Sort Key + Zone Maps work together — Sort Key makes Zone Maps effective
- Changing Sort Key = must recreate table (like DISTKEY)

---
### Real-World Use Case

Table: events — 5 billion rows, analysts always query by date range + region


```
Table: events — 5 billion rows, analysts always query by date range + region


```

Query:


```
SELECT region, SUM(value)
FROM events
WHERE event_date BETWEEN '2024-01-01' AND '2024-03-31'
  AND region = 'EAST';
  ```

- DISTKEY(region) → EAST rows already on same slices → no data movement
- SORTKEY(event_date) → Zone Maps skip all non-Q1 blocks instantly

Combined: query scans ~2% of total data instead of full table

Runs in seconds on 5 billion rows ✅