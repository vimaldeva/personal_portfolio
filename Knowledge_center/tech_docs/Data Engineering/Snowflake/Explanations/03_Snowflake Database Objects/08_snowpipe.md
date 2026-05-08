## Pipes (Snowpipe)

- Enables continuous, automatic data loading as files arrive in a stage
- No need to manually trigger COPY — Snowflake watches for new files and loads them
- Uses serverless compute — no warehouse needed

```
CREATE PIPE orders_pipe
    AUTO_INGEST = TRUE         -- triggers on S3 event notification
AS
COPY INTO orders
FROM @my_s3_stage
FILE_FORMAT = (TYPE = 'PARQUET');

-- Check pipe status
SELECT SYSTEM$PIPE_STATUS('orders_pipe');

-- Manually refresh pipe (force check for new files)
ALTER PIPE orders_pipe REFRESH;
```

### Auto-Ingest Flow (S3)



```
File lands in S3
      ↓
S3 sends SQS event notification → Snowpipe listener
      ↓
Snowpipe detects new file → triggers COPY automatically
      ↓
Data loaded into table within minutes
```

#### Key Things to Remember
- AUTO_INGEST = TRUE requires SQS notification configured on S3 bucket
- Snowpipe tracks loaded files — no duplicate loads
- Billed per file processed (serverless credits) — not per warehouse hour
- Check load history:

```
SELECT * FROM TABLE(information_schema.copy_history(
    TABLE_NAME => 'orders',
    START_TIME => DATEADD(hour, -24, CURRENT_TIMESTAMP)
));
```