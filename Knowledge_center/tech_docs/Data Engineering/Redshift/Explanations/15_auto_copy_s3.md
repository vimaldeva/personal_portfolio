## Auto-copy from S3

### What is it?
- Redshift automatically detects and loads new files dropped into an S3 path
- No need to manually trigger COPY or build a pipeline/lambda to watch S3
- Think of it as a continuous COPY job that monitors S3

Analogy:
- Manual COPY = checking your mailbox yourself every few hours
- Auto-Copy = hiring someone to watch the mailbox and bring mail the moment it arrives

---
### How it Works

```
New file lands in S3 path
        ↓
Redshift detects new file automatically
        ↓
Loads it into target table
        ↓
Tracks loaded files → never loads same file twice
```
---
### Setup

```
COPY orders
FROM 's3://bucket/orders/'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole'
FORMAT AS PARQUET
JOB CREATE auto_orders_load    -- creates the auto-copy job
AUTO ON;                        -- enables automatic triggering
```

To manually trigger the job:

```
COPY orders
FROM 's3://bucket/orders/'
IAM_ROLE '...'
JOB RUN auto_orders_load;
```

---
### Monitoring Auto-Copy Jobs
```
-- Check job status and loaded files
SELECT * FROM sys_copy_job;

-- Check load history
SELECT * FROM stl_load_commits
ORDER BY curtime DESC;
```

---
### Key Things to Remember

- Tracks already-loaded files internally → no duplicate loads
- Only picks up new files added after job creation — not existing files
- Supports same formats as COPY — Parquet, CSV, JSON, ORC
- One Auto-Copy job = one S3 prefix — create separate jobs for different paths
- Not real-time — has a small polling delay (not instant)
- If file fails to load → job continues loading other files (doesn't stop)
- Check failures in stl_load_errors as usual

---
### Auto-Copy vs Streaming Ingestion

| Factor | Auto-Copy | Streaming Ingestion |
| :-- | :-- | :-- |
| Source | S3 files | Kinesis / MSK |
| Latency | Minutes | Seconds |
| Setup | Very simple | More complex |
| Best for | File-based batch loads | Real-time event streams |

---
### Real-World Use Case

Glue ETL job runs every hour → dumps Parquet files into s3://bucket/orders/
Previously: Lambda watched S3 → triggered COPY → complex setup to maintain

With Auto-Copy:

```
COPY orders FROM 's3://bucket/orders/'
IAM_ROLE '...' FORMAT AS PARQUET
JOB CREATE hourly_orders AUTO ON;
```
Now every time Glue drops a new file → Redshift loads it automatically
No Lambda, no scheduling, no duplicate loads ✅