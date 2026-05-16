## Snowpipe (Continuous Ingestion)

### What is it?
Serverless continuous loading — loads files automatically as they arrive in a stage
No warehouse needed — uses Snowflake's serverless compute
Two triggering methods: Auto-ingest (event-based) or REST API (programmatic)

```
CREATE PIPE orders_pipe
    AUTO_INGEST = TRUE
AS
COPY INTO orders
FROM @my_s3_stage
FILE_FORMAT = (TYPE = 'PARQUET');

-- Check pipe status
SELECT SYSTEM$PIPE_STATUS('orders_pipe');

-- Pause / resume pipe
ALTER PIPE orders_pipe SET PIPE_EXECUTION_PAUSED = TRUE;
ALTER PIPE orders_pipe SET PIPE_EXECUTION_PAUSED = FALSE;

-- Force refresh (scan stage for any missed files)
ALTER PIPE orders_pipe REFRESH;
```

### Manual COPY vs Snowpipe
| Factor | COPY INTO | Snowpipe |
| :-- | :-- | :-- |
| Trigger | Manual / scheduled | Automatic (file arrival) |
| Compute | Your warehouse | Serverless |
| Latency | When you run it | Minutes after file arrives |
| Cost | Warehouse credits | Per-file serverless credits |
| File tracking | ✅ | ✅ |
| Best for | Batch loads | Continuous ingestion |