## Snowpipe Streaming

### What is it?
- Row-level streaming directly into Snowflake — no files involved
- Uses Snowflake's Ingest SDK (Java/Python)
- Much lower latency than file-based Snowpipe — sub-second to seconds

```
Traditional Snowpipe:   Records → File → S3 → Snowpipe → Table (minutes)
Snowpipe Streaming:     Records → SDK → Snowflake → Table (seconds)
```

```
# Python SDK example
from snowflake.ingest import SimpleIngestManager

# Streaming via SDK — rows pushed directly
channel = client.open_channel(
    name="orders_channel",
    database="SALES_DB",
    schema="PUBLIC",
    table="ORDERS"
)

# Insert rows directly
channel.insert_rows([
    {"ORDER_ID": 1, "REVENUE": 500.00, "ORDER_DATE": "2024-01-15"},
    {"ORDER_ID": 2, "REVENUE": 750.00, "ORDER_DATE": "2024-01-15"}
])
```

### Snowpipe vs Snowpipe Streaming
| Factor | Snowpipe | Snowpipe Streaming |
| :-- | :-- | :-- |
| Input | Files (S3/Azure/GCS) | Rows via SDK |
| Latency | 1-5 minutes | Seconds |
| Use case | File-based pipelines | Kafka, real-time apps |
| Kafka integration | Via file sink | Via Kafka Connector directly |
