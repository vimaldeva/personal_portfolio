## UPSERT Patterns (Staging Tables)

### What is it?
- UPSERT = UPDATE existing rows + INSERT new rows in one operation
- Redshift has no native UPSERT or MERGE command (unlike other databases)
- Solution: Use a Staging Table pattern to simulate UPSERT

Analogy:
- You have an employee list. New batch arrives with updates + new hires
- You can't just insert everything (duplicates) or update everything (misses new records)
- Staging table = temporary desk where you sort incoming batch first
Then replace/add to the main list cleanly

---
### How it Works

```
Incoming Data (updates + new rows)
        ↓
Load into Staging Table (temp)
        ↓
DELETE matching rows from Main Table
        ↓
INSERT all rows from Staging into Main Table
        ↓
Drop Staging Table
``` 

### Step-by-Step

Step 1 — Create Staging Table:

```
CREATE TABLE orders_staging (LIKE orders);
-- LIKE copies exact structure of main table
```

Step 2 — Load new/updated data into staging:

```
COPY orders_staging
FROM 's3://bucket/orders/updates/'
IAM_ROLE '...'
FORMAT AS PARQUET;
```

Step 3 — Delete matching rows from main table:

```
DELETE FROM orders
WHERE order_id IN (SELECT order_id FROM orders_staging);
```

Step 4 — Insert all rows from staging into main:

```
INSERT INTO orders
SELECT * FROM orders_staging;
```

Step 5 — Drop staging table:

```
DROP TABLE orders_staging;
```

---
### Wrap in a Transaction

```
BEGIN;
    DELETE FROM orders
    WHERE order_id IN (SELECT order_id FROM orders_staging);

    INSERT INTO orders
    SELECT * FROM orders_staging;
COMMIT;
```

- Wrapping in transaction ensures atomicity — either both succeed or both rollback
-No partial updates if something fails midway

---
### Key Things to Remember

- Redshift has no native MERGE/UPSERT — staging pattern is the standard way
- CREATE TABLE staging (LIKE main_table) is the cleanest way to create staging
- Always wrap DELETE + INSERT in a transaction
- Staging table is temporary — drop after use to free space
- Run VACUUM on main table after large UPSERT — ghost rows from DELETE accumulate
- For append-only data (no updates) → skip staging, just COPY directly

---
### Real-World Use Case

CRM system sends daily file with customer updates (changed emails, addresses)

- new customers added that day

Simply inserting would create duplicate customer records
Simply updating would miss new customers

Staging pattern:

- Load file into customers_staging
- Delete matched customer_id from customers
- Insert everything from staging into customers

Result: existing records updated, new records added — no duplicates ✅