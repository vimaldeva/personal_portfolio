## Streaming Ingestion (Kinesis Data Streams, MSK)

- Load data directly from streams into Redshift without landing in S3 first
- Supported sources: Kinesis Data Streams and MSK (Managed Streaming for Kafka)
- Low-latency ingestion — data available in Redshift in seconds

---
### Traditional vs Streaming Ingestion

```
Traditional (S3-based):
Stream → Firehose → S3 → COPY → Redshift
(latency: minutes to hours)

Streaming Ingestion:
Kinesis / MSK → Redshift Materialized View (seconds)
(latency: seconds)
```
---
### How it Works

```
Kinesis Stream / MSK Topic
        ↓
Redshift creates a EXTERNAL SCHEMA pointing to stream
        ↓
Materialized View reads directly from stream
        ↓
REFRESH Materialized View → data lands in Redshift
        ↓
Query the Materialized View like a normal table
```

---
### Setup (Kinesis Example)

Step 1 — Create External Schema pointing to Kinesis:

```
CREATE EXTERNAL SCHEMA kinesis_schema
FROM KINESIS
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole';
```
Step 2 — Create Materialized View to read from stream:

```
CREATE MATERIALIZED VIEW orders_stream AS
SELECT
    json_parse(kinesis_data) as data,
    partition_key,
    shard_id,
    sequence_number,
    approximate_arrival_timestamp
FROM kinesis_schema."your-stream-name";
```

Step 3 — Refresh to pull latest records:

```
REFRESH MATERIALIZED VIEW orders_stream;
-- Can be automated or triggered on schedule
```
---

### Kinesis vs MSK
| Factor | Kinesis Data Streams | MSK (Kafka) |
| :-- | :-- | :-- |
| AWS Managed | ✅ Fully | ⚠️ Partially |
| Setup complexity | Low | Higher |
| Use case | AWS-native pipelines | Kafka-based pipelines |
| Schema support | JSON | JSON, Avro |

---
### Key Things to Remember

- Data comes in as raw JSON — you parse it inside the Materialized View
- No S3 landing — stream goes directly into Redshift
- Materialized View must be refreshed to get latest data (manual or scheduled)
- Requires RA3 nodes or Serverless — not supported on DC2
- IAM Role needs permissions on Kinesis/MSK + Redshift
- Good for near real-time dashboards — not true real-time (still has seconds of lag)

---
### Real-World Use Case

E-commerce app pushes every click/order event to Kinesis
Business wants a live dashboard updating every 30 seconds

- Redshift Materialized View reads from Kinesis stream
- Scheduled job runs REFRESH MATERIALIZED VIEW every 30 seconds
- Dashboard queries the MV → sees data that is < 30 seconds old

Old approach (via S3) → data was 30-60 minutes delayed ❌
Streaming ingestion → data is seconds old ✅