## Core Foundations
- What is Apache Spark
- Spark vs MapReduce
- PySpark vs Scala Spark
- Spark Architecture (Driver, Executor, Cluster Manager)
- SparkContext vs SparkSession 
- Spark Deployment Modes (Local, Client, Cluster)
- Cluster Managers (YARN, Mesos, Kubernetes, Standalone)

SparkSession is high level for dataframe. Sparkcontext is for low level RDD

---

## Spark Core Concepts
- RDD 
- DAG (Directed Acyclic Graph)
- Lazy Evaluation
- Transformations vs Actions
- Narrow vs Wide Transformations
- Stages and Tasks
- Shuffling
- Partitions and Repartitioning
- Lineage and Fault Tolerance
- Persistence / Caching (cache vs persist)
- Storage Levels (MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY)


(Resilient Distributed Dataset) - An RDD (Resilient Distributed Dataset) is the fundamental data structure of Apache Spark. It is a distributed collection of objects partitioned across different nodes of a cluster, allowing them to be processed in parallel

When to use RDD : Unstructured Data, Low-Level Control, 
When to use DataFrame : Structured Data, Performance, SQL Queries

---

## RDD Operations
- Creating RDDs (parallelize, textFile, etc.)
- map, flatMap, filter
- reduceByKey, groupByKey, aggregateByKey, combineByKey
- sortBy, sortByKey
- join, leftOuterJoin, rightOuterJoin, fullOuterJoin, cogroup
- union, intersection, subtract, cartesian
- distinct, count, collect, take, first
- foreach, foreachPartition
- mapPartitions, mapPartitionsWithIndex
- zip, zipWithIndex
- coalesce vs repartition

---
## DataFrame & Dataset API
- DataFrame vs RDD vs Dataset
- Creating DataFrames (from CSV, JSON, Parquet, RDD, List)
- Schema — StructType, StructField, DataTypes
- InferSchema vs Explicit Schema
- show, printSchema, describe, summary
- select, filter/where, withColumn, withColumnRenamed, drop
- alias, cast
- orderBy / sort
- limit, distinct, dropDuplicates
- groupBy + agg
- pivot
- when / otherwise (conditional columns)
- isin, isNull, isNotNull
- lit (literal values)
- explode, explode_outer
- collect_list, collect_set
- array, map, struct column types

---
## Spark SQL
- Creating TempViews and GlobalTempViews
- Running SQL on DataFrames
- Catalog API
- SQL Functions vs DataFrame Functions
- Window Functions
- rank, dense_rank, row_number
- lag, lead
- sum/avg over window
- partitionBy + orderBy in window spec
- rangeBetween, rowsBetween
- Subqueries in Spark SQL
- CTEs (Common Table Expressions)

---
## Built-in Functions (pyspark.sql.functions)
- String: concat, substring, trim, upper, lower, regexp_replace, regexp_extract, split, length
- Math: round, abs, ceil, floor, pow, sqrt
- Date/Time: current_date, current_timestamp, date_add, date_sub, datediff, date_format, to_date, to_timestamp, year, month, dayofweek
- Aggregate: sum, avg, min, max, count, countDistinct, approx_count_distinct
- Array: array_contains, array_distinct, array_size, flatten, array_union, transform, filter (higher order)
- Map: map_keys, map_values
- Null handling: coalesce, nullif, nvl
- Hash: md5, sha2, crc32
- UDFs (User Defined Functions)

---
### Joins in PySpark
- Inner, Left, Right, Full Outer, Semi, Anti joins
- Cross Join
- Join on multiple conditions
- Broadcast Join (hint)
- Sort-Merge Join
- Shuffle Hash Join
- Join strategies and when Spark picks each
- Handling duplicate column names after join
- Skewed Joins and salting technique

---
### Reading & Writing Data
- DataFrameReader API
- DataFrameWriter API
- Supported formats: CSV, JSON, Parquet, ORC, Avro, Delta, JDBC
- Read options (header, inferSchema, delimiter, multiline, encoding)
- Write modes: overwrite, append, ignore, errorIfExists
- Partitioned writes (partitionBy)
- Bucketing (bucketBy)
- Reading from JDBC (databases)
- Writing to JDBC
- Reading from Hive tables
- Writing to Hive tables

---
### Partitioning & Performance
- Default Parallelism
- spark.sql.shuffle.partitions
- repartition vs coalesce
- Partition Pruning
- Predicate Pushdown
- Projection Pushdown
- Data Skew and Salting
- Broadcast Variables
- Accumulators
- Small Files Problem
- File formats comparison (Parquet vs ORC vs CSV vs Avro)
- Columnar formats and compression
- Z-Ordering (Delta Lake)

---
### Spark Execution Internals
- Query Execution Plan
- Catalyst Optimizer
- Tungsten Execution Engine
- Logical Plan → Optimized Logical Plan → Physical Plan → Execution
- explain() — simple, extended, codegen, cost, formatted
- AQE — Adaptive Query Execution
- Dynamic Partition Pruning
- Skew Join Optimization
- Coalescing shuffle partitions
- Cost-Based Optimizer (CBO)
- Whole Stage Code Generation

---
### Spark Streaming (Structured Streaming)
- Batch vs Streaming
- Micro-batch vs Continuous Processing
- Input Sources (Kafka, S3, Socket, Rate)
- Output Sinks (Console, Memory, File, Kafka, ForeachBatch)
- Output Modes (Append, Complete, Update)
- Watermarking (handling late data)
- Triggers (default, fixed interval, once, availableNow)
- Stateful Operations
- Streaming Aggregations
- Stream-Stream Joins
- Stream-Static Joins
- Checkpointing

---
### Delta Lake (Important for Real-World)
- What is Delta Lake
- ACID transactions in Spark
- Delta Table vs Parquet Table
- Transaction Log (_delta_log)
- Read and Write Delta Tables
- MERGE (Upsert) operation
- UPDATE and DELETE operations
- Time Travel (VERSION AS OF, TIMESTAMP AS OF)
- Schema Evolution (mergeSchema, overwriteSchema)
- Schema Enforcement
- Optimize and ZORDER
- Vacuum
- Delta Table History
- Change Data Feed (CDF)
- Delta Live Tables (DLT)

---
### UDFs (User Defined Functions)
- Python UDF (regular)
- Pandas UDF (Vectorized UDF) — SCALAR, GROUPED_MAP, GROUPED_AGG
- UDF vs Built-in functions (performance implications)
- Registering UDFs for SQL use
- Return types in UDFs

---
### Schema Handling
- StructType and StructField
- Nested schemas (StructType within StructType)
- ArrayType and MapType
- Reading nested JSON
- Flattening nested structures
- Schema evolution
- Schema merging

---
### Configuration & Tuning
- SparkConf and spark-submit configs
- Key configs to know:
    - spark.executor.memory
    - spark.executor.cores
    - spark.driver.memory
    - spark.sql.shuffle.partitions
    - spark.default.parallelism
    - spark.sql.autoBroadcastJoinThreshold
    - spark.memory.fraction
    - spark.speculation
- Dynamic Resource Allocation
- Memory management (Execution vs Storage memory)
- GC tuning basics
- Kryo Serialization

---
### Error Handling & Debugging
- Reading Spark UI
- Jobs, Stages, Tasks tabs
- DAG visualization
- Storage tab (cached RDDs/DFs)
- Executors tab
- SQL tab (query plans)
- Common errors: OOM, GC overhead, Shuffle fetch failed
- Handling corrupt records (PERMISSIVE, DROPMALFORMED, FAILFAST)
- try/except in PySpark
- Logging in Spark jobs

---
### PySpark with Cloud & Ecosystem
- PySpark on EMR
- PySpark on Databricks
- PySpark on Glue
- PySpark on Dataproc (GCP)
- Connecting to S3, ADLS, GCS
- Reading from Redshift via Spark
- Reading from Snowflake via Spark
- Hive Metastore integration
- Unity Catalog (Databricks)

---
### Testing PySpark Code
- Unit testing with pytest
- Mocking SparkSession in tests
- chispa library (DataFrame equality checks)
- pytest-spark
- Testing UDFs

---
### Scenarios You Must Know How to Handle

#### Data Quality

- Handle null values in large datasets
- Handle schema mismatches between files
- Handle corrupt/malformed records during read
- Deduplicate records efficiently at scale

#### Performance

- Fix OOM errors on executor
- Fix OOM errors on driver (collect() on large data)
- Fix data skew in joins and aggregations
- Optimize shuffle-heavy jobs
- Reduce number of small output files

#### Joins

- Join two massive tables without shuffle (broadcast)
- Handle skewed join keys (salting)
- Join streaming data with static lookup table

#### Streaming

- Handle late arriving data with watermarks
- Exactly-once processing with checkpointing
- Aggregate streaming data over sliding/tumbling windows

#### Delta Lake

- Upsert (MERGE) incoming CDC data into Delta table
- Roll back accidental deletes using Time Travel
- Handle schema evolution without breaking downstream jobs
- Compact small files with OPTIMIZE + ZORDER

#### Real-World Pipelines

- Build incremental ETL pipeline (process only new data)
- Flatten deeply nested JSON from API responses
- Partition large datasets efficiently for downstream queries
- Read and write to JDBC without overwhelming source DB