## Manifest Files

### What is it?
- A JSON file that explicitly lists which S3 files should be loaded by the COPY command
- Instead of pointing COPY to an entire S3 prefix (folder), you control exactly which files load

Analogy:
- Without manifest = telling movers "take everything from that warehouse"
- With manifest = giving movers a specific checklist of items to take

---
### Why it Matters
- Avoid accidentally loading wrong or extra files from a shared S3 prefix
- Load files from multiple S3 locations/buckets in one COPY command
- Mark files as mandatory — COPY fails if that file is missing (data quality check)
- Useful for reprocessing specific files without reloading everything

---
### Manifest File Structure

```
{
  "entries": [
    {"url": "s3://bucket/orders/orders_part1.csv", "mandatory": true},
    {"url": "s3://bucket/orders/orders_part2.csv", "mandatory": true},
    {"url": "s3://other-bucket/orders_part3.csv",  "mandatory": false}
  ]
}
```

- mandatory: true → COPY fails if file not found
- mandatory: false → COPY skips if file not found, continues loading

---

### Using Manifest in COPY

```
COPY orders
FROM 's3://bucket/manifests/orders_manifest.json'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole'
FORMAT AS CSV
MANIFEST;
```

---
### Key Things to Remember

- Manifest file itself must be stored in S3
- Can reference files across different S3 buckets or prefixes
mandatory: true is a built-in data quality guard
- Without MANIFEST keyword in COPY → Redshift treats the file as a regular data file not a manifest
- Glue and other ETL tools often auto-generate manifests for controlled Redshift loads

---
### Real-World Use Case
Daily pipeline generates files in S3 alongside other files from different pipelines
Directly pointing COPY to the folder would load unwanted files

Solution: ETL job generates a manifest listing only today's order files

```
{"entries": [
  {"url": "s3://datalake/raw/orders_20240115_1.parquet", "mandatory": true},
  {"url": "s3://datalake/raw/orders_20240115_2.parquet", "mandatory": true}
]}
```
COPY loads exactly these files — nothing more, nothing less ✅

