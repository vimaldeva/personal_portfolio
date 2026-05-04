## UNLOAD Command

### What is it?

- Exports query results from Redshift to S3
- Opposite of COPY — COPY loads data in, UNLOAD pushes data out
- Exports in parallel across all slices — fast for large datasets

Analogy:
- COPY = Importing goods into a warehouse
- UNLOAD = Exporting goods out of the warehouse to a destination

```
UNLOAD ('SELECT * FROM orders WHERE order_date = ''2024-01-15''')
TO 's3://bucket/exports/orders/'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole'
FORMAT AS PARQUET;
```

---
### How it Works

```
Redshift runs the SELECT query
        ↓
Each slice writes its portion of results to S3 in parallel
        ↓
Multiple files created in S3 (one per slice)

Result in S3:
├── orders_0000_part00.parquet   ← Slice 1 output
├── orders_0001_part00.parquet   ← Slice 2 output
├── orders_0002_part00.parquet   ← Slice 3 output
└── orders_0003_part00.parquet   ← Slice 4 output
```

### Common Options

```
FORMAT AS PARQUET          -- export as Parquet (recommended)
FORMAT AS CSV              -- export as CSV
DELIMITER ','              -- CSV delimiter
HEADER                     -- include column headers in CSV
GZIP                       -- compress output files
PARALLEL OFF               -- export as single file (slow, use carefully)
ALLOWOVERWRITE             -- overwrite existing files in S3 path
MAXFILESIZE 100 MB         -- control output file size
PARTITION BY (order_date)  -- partition output by column value
```

---
### Key Things to Remember

- By default produces multiple files (parallel) — one per slice
- PARALLEL OFF → single file → slow, only for small result sets
- Always use Parquet + compression for large exports — smaller files, faster
- S3 path must be empty unless ALLOWOVERWRITE is specified
- IAM Role needs s3:PutObject permission on target bucket
- PARTITION BY creates Hive-style partitions in S3 — great for Athena/Spectrum queries
- UNLOAD does not delete data from Redshift — just copies it out

---
### COPY vs UNLOAD

| Factor | COPY | UNLOAD |
| :-- | :-- | :-- |
| Direction | S3 → Redshift | Redshift → S3 |
| Purpose | Load data in | Export data out |
| Parallelism | ✅ Yes | ✅ Yes |

---
### Real-World Use Case

Data team wants to share last month's orders with Data Science team
Data Science uses S3 + Athena — not Redshift

```
UNLOAD ('SELECT * FROM orders WHERE order_date >= ''2024-01-01''')
TO 's3://data-share/orders/jan2024/'
IAM_ROLE '...'
FORMAT AS PARQUET
PARTITION BY (region)
ALLOWOVERWRITE;
```

Exports in parallel → fast even for billions of rows
Partitioned by region → Athena queries only relevant partitions ✅

Data Science team queries directly from S3 — no Redshift access needed

