## COPY Command

- Fastest way to load data into Redshift from external sources
- Loads data in parallel across all slices simultaneously
- Always prefer over INSERT for bulk loading

Analogy:
INSERT = moving house one item at a time in your car
COPY = hiring a moving truck that loads everything in parallel

---
### Basic Syntax

```
COPY table_name
FROM 's3://bucket-name/path/'
IAM_ROLE 'arn:aws:iam::account-id:role/RedshiftRole'
FORMAT AS PARQUET;
```

---
### How Parallel Loading Works

```
S3 Files split into parts:
├── orders_part1.csv  → Slice 1
├── orders_part2.csv  → Slice 2
├── orders_part3.csv  → Slice 3
└── orders_part4.csv  → Slice 4

All slices load simultaneously → fast
```
- Best practice: Number of S3 files = Total slices in cluster
- Single large file = only 1 slice works → rest idle → slow

---
### Supported Sources & Formats
- Sources: S3 (most common), DynamoDB, EMR, SSH
- Formats: CSV, JSON, Parquet, ORC, GZIP/compressed files

---
### Key Options to Know


```
IGNOREHEADER 1        -- skip header row
MAXERROR 100          -- tolerate up to 100 bad rows before failing
EMPTYASNULL           -- treat empty strings as NULL
TRUNCATECOLUMNS       -- truncate values exceeding column length
MANIFEST              -- load specific files listed in a manifest JSON
```

---
### Checking Errors

```
SELECT * FROM stl_load_errors
ORDER BY starttime DESC;
```

---
### Key Things to Remember

- Uses IAM Role for S3 access — not hardcoded credentials
- Split input files to match total slice count for max parallelism
- Auto-detects compression (GZIP, SNAPPY, ZSTD)
- Automatically runs ANALYZE and sets compression encodings after load
- Run VACUUM after loading into an existing sorted table

---
### Real-World Use Case
Nightly ETL dumps 50M rows as 16 Parquet files → cluster has 16 slices


```
COPY orders
FROM 's3://data-lake/orders/2024/01/15/'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole'
FORMAT AS PARQUET;
```

16 files → 16 slices → all load simultaneously → 50M rows in ~2 minutes
Same via INSERT row-by-row → 4+ hours

---
// give me sample copy command
```
COPY sales
FROM 's3://my-bucket/sales_data/'
IAM_ROLE 'arn:aws:iam::123456789012:role/MyRedshiftRole'
FORMAT AS CSV
IGNOREHEADER 1
MAXERROR 10
EMPTYASNULL

```

// In the above copy command , what does sales denote ?, does it refer to the table that will be newly creatred on redshift based on the files ?

Yes, in the COPY command, "sales" refers to the name of the target table in Redshift where the data will be loaded. This table must already exist in Redshift before you run the COPY command. The command will load the data from the specified S3 location into the existing "sales" table. If the table does not exist, you would need to create it first using a CREATE TABLE statement before executing the COPY command.
