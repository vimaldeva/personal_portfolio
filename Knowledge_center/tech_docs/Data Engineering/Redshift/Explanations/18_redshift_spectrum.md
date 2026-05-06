## Redshift Spectrum (External Tables)

## What is it?
- Query data directly in S3 without loading it into Redshift
- Data stays in S3 — Redshift just reads it on-demand
- Uses Glue Data Catalog (or Hive Metastore) to store table metadata

Analogy:

Instead of bringing books into your office (loading to Redshift)
You go to the library and read them there (query S3 directly)

```
Redshift Query
      ↓
Leader Node sees external table reference
      ↓
Spectrum Layer spins up (separate compute — not your cluster)
      ↓
Reads S3 files in parallel
      ↓
Returns results back to Redshift
```

```
-- Create external schema pointing to Glue Catalog
CREATE EXTERNAL SCHEMA spectrum_schema
FROM DATA CATALOG
DATABASE 'glue_db'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole';

-- Query external table directly
SELECT * FROM spectrum_schema.orders
WHERE order_date = '2024-01-15';
```

### Key Things to Remember

- Spectrum has separate pricing — charged per TB scanned
- Use Parquet + Partitioning to minimize data scanned = lower cost
- Can JOIN Redshift tables with Spectrum external tables
- Best for cold/historical data too large or rarely accessed to load into Redshift
- Spectrum compute is separate from your cluster — doesn't affect cluster performance

