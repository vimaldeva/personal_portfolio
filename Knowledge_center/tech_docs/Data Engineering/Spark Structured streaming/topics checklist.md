### Core Concepts
What is Structured Streaming
Streaming vs Batch processing
Micro-batch vs Continuous Processing
Unbounded Table concept
Input Table, Results Table, Output Table
Event Time vs Processing Time vs Ingestion Time
Fault Tolerance in Structured Streaming
Exactly-once semantics
At-least-once semantics

---

### SparkSession for Streaming
Creating SparkSession for streaming
spark.readStream vs spark.read
df.isStreaming property
Streaming DataFrame vs Static DataFrame

---
### Input Sources
File Source (CSV, JSON, Parquet, ORC from directory)
Kafka Source (most common in production)
Socket Source (dev/testing only)
Rate Source (generates data at fixed rate — testing)
Rate Per Micro-batch Source
Delta Lake Source
Kinesis Source (AWS — via connector)
Source options and configurations per source type

---
### Kafka Integration (Deep)
Kafka Source configuration
subscribe vs subscribePattern vs assign
startingOffsets (earliest, latest, specific)
endingOffsets
Reading value as binary → casting to string
Deserializing JSON from Kafka value
Schema for Kafka DataFrame (key, value, topic, partition, offset, timestamp)
Reading Kafka headers
Writing back to Kafka (Kafka Sink)
kafka.bootstrap.servers
SSL / SASL authentication with Kafka
Schema Registry + Avro deserialization

---
### Output Sinks
Console Sink (dev/debug only)
Memory Sink (dev/debug — stores in memory table)
File Sink (CSV, JSON, Parquet — append only)
Kafka Sink (write stream back to Kafka topic)
Delta Lake Sink (most common in production)
ForeachBatch Sink (custom logic per micro-batch)
Foreach Sink (row-level custom processing)

---
### Output Modes
Append Mode — only new rows written since last trigger
Complete Mode — entire result table written every trigger
Update Mode — only rows that changed since last trigger
Which mode works with which operations
Aggregations + output mode compatibility

---
### Triggers
Default (unspecified) — runs micro-batch as fast as possible
Fixed Interval — processingTime = "30 seconds"
Once — runs one micro-batch then stops (legacy)
AvailableNow — processes all available data then stops (replaces Once)
Continuous — experimental low-latency mode
Trigger behavior with no new data

---
### Watermarking
What is a Watermark
Late arriving data problem
withWatermark(column, delay) syntax
How watermark advances over time
Effect of watermark on state cleanup
Watermark with aggregations
Watermark with joins
Global watermark in multi-source streams
Watermark and output modes compatibility

---
### Stateful Operations
Stateful vs Stateless operations
State store concept
State store backends (HDFS, RocksDB)
RocksDB state store (performance)
State size management
State cleanup and TTL
mapGroupsWithState (arbitrary stateful processing)
flatMapGroupsWithState (with timeout support)
Timeout types (ProcessingTimeTimeout, EventTimeTimeout)

---
### Streaming Aggregations
groupBy + agg on streams
Window functions on streams (tumbling, sliding, session)
Tumbling Window — fixed non-overlapping windows
Sliding Window — overlapping windows
Session Window — dynamic gap-based windows
window() function
session_window() function
Window + Watermark combination
Count, Sum, Avg, Min, Max on streams
approx_count_distinct for streaming
Aggregations without watermark (unbounded state)

---
### Stream-Static Joins
Joining streaming DataFrame with static DataFrame
Static DataFrame reloaded each trigger or cached
Supported join types (inner, left outer)
Use case: enrich stream with lookup table
Limitations of stream-static joins

---
### Stream-Stream Joins
Joining two streaming DataFrames
Watermark requirement for stream-stream joins
Inner join with watermark
Left outer join with watermark
State management in stream-stream joins
Join condition with event time bounds
Supported and unsupported join types

---
### ForeachBatch
What is ForeachBatch
Writing each micro-batch as a regular DataFrame
Use cases: upsert to Delta, write to JDBC, multiple sinks
batchId parameter
Idempotent writes using batchId
Reusing batch DataFrame multiple times (cache inside foreachBatch)

```
def process_batch(batch_df, batch_id):
    batch_df.cache()
    batch_df.write.format("delta").mode("append").save(...)
    batch_df.write.format("jdbc").mode("append").save(...)
    batch_df.unpersist()

stream.writeStream.foreachBatch(process_batch).start()

```
---
### Checkpointing
What is a checkpoint
Checkpoint location setup
What checkpoint stores (offsets, state, metadata)
Checkpoint and fault tolerance
Recovering from failure using checkpoint
Checkpoint location on S3 / HDFS / ADLS
Schema changes and checkpoint compatibility
When to delete and restart checkpoint

---
### Offsets & Progress
StreamingQuery object
query.lastProgress — last micro-batch stats
query.status — current status
query.recentProgress — list of recent batches
query.awaitTermination() — block until stream stops
query.stop() — gracefully stop stream
Offset tracking per source
StreamingQueryListener — monitoring events programmatically

---
### Schema & Schema Evolution
Schema inference in streaming (usually avoid)
Explicit schema definition for streams
Schema enforcement
Schema evolution with Delta Lake sink
Handling schema mismatch in Kafka messages
from_json() for parsing JSON strings
to_json() for serializing to JSON

---
### Error Handling in Streaming
What happens when a micro-batch fails
Retry behavior
failOnDataLoss option (Kafka)
Corrupt record handling
Dead letter queue pattern
Try/except inside foreachBatch

---
### Performance & Tuning
maxFilesPerTrigger (file source)
maxOffsetsPerTrigger (Kafka source)
maxBytesPerTrigger (Delta source)
Trigger interval tuning
State store tuning
RocksDB state backend vs default HDFS
Repartitioning streams
Shuffle partitions for streaming (spark.sql.shuffle.partitions)
Micro-batch latency tuning
Backpressure concept

---
### Monitoring & Debugging
Spark UI for streaming (Structured Streaming tab)
Input Rate vs Processing Rate
Batch Duration
State operator metrics
query.lastProgress JSON output
StreamingQueryListener implementation
Prometheus / Grafana integration
Logging micro-batch progress

---
### Delta Lake + Streaming (Production Pattern)
Delta as streaming source (readStream from Delta)
Delta as streaming sink (writeStream to Delta)
ignoreChanges option
ignoreDeletes option
startingVersion and startingTimestamp
maxBytesPerTrigger and maxFilesPerTrigger for Delta source
MERGE inside foreachBatch (upsert pattern)
Delta + Autoloader combination

---
### Autoloader (Databricks / AWS)
What is Autoloader
Autoloader vs manual file stream
cloudFiles format
File notification mode (SQS/SNS on AWS)
Directory listing mode
Schema inference and evolution with Autoloader
cloudFiles.schemaLocation
Autoloader + Delta sink (standard production pattern)

---
### Kinesis + Structured Streaming (AWS Specific)
Kinesis as streaming source
kinesis format
streamName, region, initialPosition
startingPosition (TRIM_HORIZON, LATEST, AT_TIMESTAMP)
Kinesis shard reading
Kinesis connector setup on EMR / Glue
Throughput limits and shard splitting

---
### Production Patterns & Scenarios

#### Ingestion Patterns

Kafka → Delta Lake (standard streaming ETL)
S3 files → Delta Lake (Autoloader pattern)
Kinesis → Delta Lake (AWS streaming)
Kafka → Kafka (stream transformation)
Processing Patterns

#### Real-time aggregations with watermark
Sessionization with session windows
Deduplication (dropDuplicates on stream)
Streaming joins with enrichment table
CDC processing (inserts/updates/deletes)
Sink Patterns

#### Upsert to Delta using MERGE in foreachBatch
Write to multiple sinks in one foreachBatch
Write to JDBC (database) from stream
Write back to Kafka after transformation
Reliability Patterns

#### Exactly-once with Delta + checkpoint
Idempotent foreachBatch using batchId
Dead letter queue for bad records
Schema validation before writing
Graceful shutdown handling

---
### Key Terminologies Quick Reference
| Term | Meaning |
| :-- | :-- |
| Micro-batch | Small batch of data processed at each trigger interval |
| Watermark | Threshold for how late data can arrive |
| State Store | Where streaming state (aggregations) is persisted |
| Checkpoint | Saved progress — enables recovery after failure |
| Trigger | How often a micro-batch runs |
| Offset | Position in source (Kafka partition, file list) |
| Sink | Destination where results are written |
| Source | Where streaming data comes from |
| StreamingQuery | Handle to a running stream — monitor and control |
| Event Time | Timestamp embedded in the data itself |
| Processing Time | When Spark actually processes the record |
| Tumbling Window | Fixed size, non-overlapping time windows |
| Sliding Window | Fixed size, overlapping time windows |
| Session Window | Dynamic window based on activity gaps |
| ForeachBatch | Custom function applied to each micro-batch DataFrame |
| AvailableNow | Process all backlog then stop — replaces .once() |