## Metadata Layer

### What is it?
- A global metadata store managed entirely by Snowflake's Cloud Services layer
- Stores information about your data — not the actual data itself
- Lives outside of storage and compute — always available, always fast

---
### What Metadata Snowflake Stores

```
For every micro-partition:
├── Row count
├── MIN and MAX value per column
├── NULL count per column
├── Distinct value count per column
├── File location in S3/Azure/GCS
└── Encryption keys

For every table:
├── Schema definition
├── Column data types
├── Clustering information
├── Total row count
└── Table size

For queries:
├── Query history
├── Execution plans
├── Compilation cache
└── Result cache references
```

---
### Why Metadata Layer Matters

```
-- These queries answered PURELY from metadata — ZERO data scanned:
SELECT COUNT(*) FROM orders;            -- row count in metadata
SELECT MIN(order_date) FROM orders;     -- MIN stored in metadata
SELECT MAX(revenue) FROM orders;        -- MAX stored in metadata
```

- No warehouse needed for metadata-only queries → free to run
- Partition pruning decisions made entirely from metadata — no data read
- This is why Snowflake can prune partitions so fast

---
### Key Things to Remember
- Metadata is stored in Cloud Services layer — always on, always fast
- COUNT(*), MIN, MAX on full table = answered from metadata, no compute cost
- Metadata is updated automatically on every DML operation
- You cannot directly access raw metadata — but you can query via INFORMATION_SCHEMA and ACCOUNT_USAGE

```
-- Query metadata-backed views
SELECT * FROM information_schema.tables;
SELECT * FROM information_schema.columns;
SELECT SYSTEM$CLUSTERING_INFORMATION('orders', '(order_date)');
```