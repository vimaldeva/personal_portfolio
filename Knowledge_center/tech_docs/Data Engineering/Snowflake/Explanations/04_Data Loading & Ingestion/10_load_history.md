## Load History

### What is it?
- Snowflake tracks every file loaded via COPY — prevents duplicate loads
- Tracked at pipe level (Snowpipe) or table level (COPY INTO)
- Check Load History

```
-- COPY INTO load history (last 14 days via INFORMATION_SCHEMA)
SELECT *
FROM TABLE(information_schema.copy_history(
    TABLE_NAME => 'ORDERS',
    START_TIME => DATEADD(hours, -24, CURRENT_TIMESTAMP)
));

-- Snowpipe load history
SELECT *
FROM TABLE(information_schema.copy_history(
    TABLE_NAME => 'ORDERS',
    START_TIME => DATEADD(days, -7, CURRENT_TIMESTAMP)
));

-- Long-term history (up to 1 year — ACCOUNT_USAGE)
SELECT *
FROM snowflake.account_usage.copy_history
WHERE table_name = 'ORDERS'
  AND last_load_time >= DATEADD(days, -30, CURRENT_TIMESTAMP)
ORDER BY last_load_time DESC;
```

### Key Columns in Copy History
| Column | What it Tells You |
| :-- | :-- |
| file_name | Which file was loaded |
| status | LOADED, LOAD_FAILED, PARTIALLY_LOADED |
| rows_loaded | How many rows successfully loaded |
| errors_seen | Number of error rows |
| first_error | Description of first error |
| last_load_time | When file was loaded |

### Load History Retention
| Method | Retention |
| :-- | :-- |
| INFORMATION_SCHEMA.COPY_HISTORY | 14 days |
| ACCOUNT_USAGE.COPY_HISTORY | 1 year |
| Snowpipe metadata (dedup tracking) | 14 days |

### Real-World Loading Pipeline
```
-- Step 1: Validate before loading
COPY INTO orders FROM @my_s3_stage
FILE_FORMAT = (FORMAT_NAME = 'parquet_fmt')
VALIDATION_MODE = 'RETURN_ERRORS';

-- Step 2: Fix errors if any, then load
COPY INTO orders FROM @my_s3_stage
FILE_FORMAT = (FORMAT_NAME = 'parquet_fmt')
ON_ERROR = 'CONTINUE'       -- skip bad rows
PURGE = TRUE;               -- delete files after load

-- Step 3: Check what was loaded
SELECT file_name, status, rows_loaded, errors_seen
FROM TABLE(information_schema.copy_history(
    TABLE_NAME => 'ORDERS',
    START_TIME => DATEADD(minutes, -10, CURRENT_TIMESTAMP)
));
```

Files with errors → check stl_load_errors equivalent
Rows skipped logged in copy history → fix source and reload with FORCE = TRUE 