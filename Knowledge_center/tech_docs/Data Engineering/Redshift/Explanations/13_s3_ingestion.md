## S3 Ingestion

## What is it?
- Loading data from S3 into Redshift tables using the COPY command
- Most common and recommended ingestion pattern for Redshift
- S3 acts as a staging/landing zone before data enters Redshift

---
###     How it Works

```
Source (DB, App, Logs)
        ↓
Data lands in S3 (CSV / JSON / Parquet)
        ↓
COPY Command triggers
        ↓
Each slice pulls files directly from S3 in parallel
        ↓
Data loaded into Redshift table
```

---
### File Format Recommendations

| Format | Recommended? | Why |
| :-- | :-- | :-- |
| Parquet | ✅ Best | Columnar, compressed, fast |
| ORC | ✅ Good | Similar to Parquet |
| CSV (GZIP) | ⚠️ OK | Simple but not columnar |
| JSON | ❌ Avoid for large loads | Verbose, slow to parse |

---
### Best Practices for S3 Ingestion
- Split files to match number of slices → max parallelism
- Use Parquet over CSV where possible → less data to transfer
- Compress files (GZIP, SNAPPY, ZSTD) → faster transfer, less S3 cost
- Partition S3 data by date/region → load only relevant partitions
- Use Manifest when folder has mixed files

---
### IAM Setup for S3 Access

```
Redshift Cluster
    └── Attached IAM Role
            └── Policy allows:
                    s3:GetObject
                    s3:ListBucket
                    kms:Decrypt  (if files are KMS encrypted)
```
Always use IAM Role — never hardcode access keys in COPY command

---
### Auto-Copy (S3 Auto COPY)

- New feature — Redshift automatically detects new files in S3 and loads them
- No need to trigger COPY manually or build a pipeline
- Like a continuous listener on an S3 path

```
CREATE TABLE orders (...);

COPY orders
FROM 's3://bucket/orders/'
IAM_ROLE '...'
FORMAT AS PARQUET
JOB CREATE auto_orders_load
AUTO ON;
```
---
### Key Things to Remember
- S3 → Redshift is a pull model — Redshift pulls files from S3 (not pushed)
- Enhanced VPC Routing forces traffic through VPC instead of public internet — more secure
- Large single files = slow (only 1 slice loads) → always split before loading
- For incremental loads → either partition S3 by date or use Manifest to target specific files
- Failed loads → check stl_load_errors

---
### Real-World Use Case
App events are streamed → Kinesis Firehose → lands as Parquet files in S3 every 5 mins
Partitioned as: s3://bucket/events/year=2024/month=01/day=15/

Nightly job runs:
```
COPY events
FROM 's3://bucket/events/year=2024/month=01/day=15/'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole'
FORMAT AS PARQUET;
```

Only today's partition loaded → no reprocessing old data → fast and efficient ✅

