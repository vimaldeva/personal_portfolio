## Tables

### Four Table Types

### Permanent Table (Default)
- Full Time Travel + Fail-safe
- Data persists until explicitly dropped
- Highest storage cost

```
CREATE TABLE orders (
    order_id    NUMBER,
    order_date  DATE,
    revenue     DECIMAL(10,2)
);
```

### Temporary Table
- Session-scoped — automatically dropped when session ends
- No Fail-safe, Time Travel 0-1 day
- Not visible to other sessions — private to your session
- Good for: intermediate ETL results, session-level temp data

```
CREATE TEMPORARY TABLE temp_orders AS
SELECT * FROM orders WHERE order_date = CURRENT_DATE;
-- Disappears when you disconnect
```

### Transient Table
- Persists across sessions (unlike temporary)
- No Fail-safe, Time Travel 0-1 day
- Lower storage cost than permanent
- Good for: staging tables, data you can reload if lost

```
CREATE TRANSIENT TABLE staging_orders (
    order_id   NUMBER,
    order_date DATE
);
```
### External Table
- Metadata layer over files in S3/Azure/GCS — data stays in cloud storage
- Read-only — cannot INSERT/UPDATE/DELETE
- Good for: querying data lake files without loading into Snowflake

```
CREATE EXTERNAL TABLE ext_orders (
    order_id   NUMBER AS (VALUE:order_id::NUMBER),
    order_date DATE   AS (VALUE:order_date::DATE)
)
WITH LOCATION = @my_s3_stage
FILE_FORMAT = (TYPE = 'PARQUET');
```

| Feature | Permanent | Temporary | Transient | External |
| :-- | :-- | :-- | :-- | :-- |
| Persists after session | ✅ | ❌ | ✅ | ✅ |
| Time Travel | 0-90 days | 0-1 day | 0-1 day | ❌ |
| Fail-safe | ✅ 7 days | ❌ | ❌ | ❌ |
| Storage cost | Highest | Low | Medium | Lowest |
| DML allowed | ✅ | ✅ | ✅ | ❌ |
| Use case | Production | Session temp | Staging | Data lake |


