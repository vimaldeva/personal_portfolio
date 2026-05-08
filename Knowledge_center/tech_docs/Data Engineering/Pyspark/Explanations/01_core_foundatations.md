# Core Foundations


## What is Apache Spark
- Distributed data processing engine for large-scale data
- Processes data in-memory across a cluster of machines in parallel
- Can handle batch, streaming, ML, and graph processing — all in one engine

Analogy:

Processing 1TB data on one machine = one person reading 1 million pages
Spark = 1000 people each reading 1000 pages simultaneously

### Key Things to Remember
- Spark is written in Scala — PySpark is the Python API on top
- Core concept: distribute data + process in parallel
- Works on top of cluster managers (YARN, Kubernetes etc.)
- Does NOT store data — it processes data from S3, HDFS, databases etc.

---
## Spark vs MapReduce

Key Differences

| Factor | MapReduce | Spark |
| :-- | :-- | :-- |
| Processing | Disk-based (reads/writes disk between steps) | In-memory (keeps data in RAM) |
| Speed | Slow (heavy disk I/O) | Up to 100x faster |
| Ease of use | Complex (Java, verbose) | Simple (Python, Scala, SQL) |
| Real-time streaming | ❌ No | ✅ Yes |
| ML support | ❌ Limited | ✅ MLlib built-in |
| Fault tolerance | Recompute from disk | Recompute via lineage (RDD) |

### Why Spark Won

```
MapReduce pipeline (3 steps):
Step1 → write to disk → Step2 → write to disk → Step3 → write to disk

Spark pipeline (3 steps):
Step1 → in memory → Step2 → in memory → Step3 → write to disk ONCE
```

---
## PySpark vs Scala Spark
What's the Difference?


| Factor | PySpark | Scala Spark |
| :-- | :-- | :-- |
| Language | Python | Scala |
| Performance | Slightly slower (Python overhead) | Faster (native JVM) |
| UDF Performance | Slower (serialization between JVM ↔ Python) | Fast (runs on JVM directly) |
| Ease of use | ✅ Easier, more data scientists use it | Steeper learning curve |
| Pandas UDF | ✅ Bridges performance gap | N/A |
| Industry adoption | ✅ More common (data engineering/science) | Used in performance-critical jobs |

### Key Things to Remember
- For DataFrame/SQL operations — PySpark performance is nearly identical to Scala
- Performance gap only matters for Python UDFs (avoid regular UDFs, use Pandas UDF)
- Most data engineers use PySpark — Scala Spark only when extreme performance needed
- Same underlying engine — just different API layer

---
## Spark Architecture

```
┌─────────────────────────────────────────────┐
│              DRIVER NODE                     │
│  - Your PySpark script runs here             │
│  - Creates SparkSession                      │
│  - Builds DAG (execution plan)               │
│  - Coordinates executors                     │
│  - Collects final results                    │
└──────────────────┬──────────────────────────┘
                   │ talks to
┌──────────────────▼──────────────────────────┐
│           CLUSTER MANAGER                    │
│  - Allocates resources (CPU, RAM)            │
│  - YARN / Kubernetes / Mesos / Standalone    │
└──────┬───────────┬──────────────┬────────────┘
       │           │              │
┌──────▼──┐  ┌─────▼───┐  ┌──────▼──┐
│Executor │  │Executor │  │Executor │   ← worker nodes
│ Task1   │  │ Task1   │  │ Task1   │
│ Task2   │  │ Task2   │  │ Task2   │
│ Cache   │  │ Cache   │  │ Cache   │
└─────────┘  └─────────┘  └─────────┘
```

#### Driver
- Brain of the Spark application
- Runs your code, creates execution plan, schedules tasks
- If driver dies → entire job fails
- Has Driver Memory — don't collect() huge datasets here

#### Executor
- Workers that actually process data
- Each executor has CPU cores (slots for tasks) + memory
- Tasks run in parallel across executor cores
- If executor dies → Spark retries tasks (fault tolerant)
#### Cluster Manager
- Manages resource allocation across the cluster
- Driver requests resources → Cluster Manager assigns executors

### Key Things to Remember
- 1 Spark Application = 1 Driver + Multiple Executors
- More executor cores = more tasks run in parallel
- Executor memory split: Execution memory (processing) + Storage memory (caching)
- Driver is a bottleneck if you collect() large data — it all flows back to driver

---
## SparkContext vs SparkSession

### SparkContext (Old — Spark 1.x)
- Entry point for RDD-based operations
- One SparkContext per JVM
- Used to create RDDs, access cluster

```
from pyspark import SparkContext
sc = SparkContext(appName="MyApp")
rdd = sc.parallelize([1, 2, 3, 4])
```

### SparkSession (New — Spark 2.x+ ✅)
- Unified entry point for everything — RDDs, DataFrames, SQL, Streaming
- Internally creates SparkContext for you
- Use this in all modern PySpark code

```
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Access SparkContext through SparkSession
sc = spark.sparkContext
```

### Key Things to Remember
- Always use SparkSession in modern PySpark — SparkContext is legacy
- getOrCreate() — returns existing session if one exists, creates new if not
- One SparkSession per application (but can create multiple with different configs using .newSession())
- SparkSession gives access to: spark.read, spark.sql, spark.catalog, spark.sparkContext

---
## Spark Deployment Modes
### Local Mode (Development)
- Everything runs on your single machine
- No cluster needed — driver + executor in same JVM
- Used for development and testing
```
spark = SparkSession.builder \
    .master("local")      # 1 core
    .master("local[4]")   # 4 cores
    .master("local[*]")   # all available cores
    .getOrCreate()
```
### Client Mode (Interactive)
- Driver runs on your machine (client)
- Executors run on cluster nodes
- Used for interactive sessions (notebooks, Jupyter)

```
Your Laptop (Driver)  ←→  Cluster (Executors)
```

- If you close laptop/terminal → job dies (driver is on your machine)
- Good for: Databricks notebooks, EMR notebooks, interactive debugging

### Cluster Mode (Production)
- Both Driver and Executors run on cluster
- You submit job and disconnect — job runs independently
- Used for production scheduled jobs

```
spark-submit --deploy-mode cluster my_job.py

Your Machine → submits → Cluster (Driver + Executors run here)
You can disconnect — job continues ✅
```

| Mode | Driver Location | Best For |
| :-- | :-- | :-- |
| Local | Your machine | Development/Testing |
| Client | Your machine | Interactive notebooks |
| Cluster | Cluster node | Production jobs |


---
## Cluster Managers

### What is it?
- Responsible for allocating and managing resources (CPU, memory) across worker nodes
- Spark doesn't care which cluster manager you use — pluggable architecture

### YARN (Yet Another Resource Negotiator)
- Part of Hadoop ecosystem
- Most common in on-premise and EMR setups
- ResourceManager allocates containers to Spark executors

```
Common setup: EMR + YARN
spark-submit --master yarn --deploy-mode cluster my_job.py
```

### Which to Use?

| Scenario | Cluster Manager |
| :-- | :-- |
| AWS EMR | YARN |
| Databricks | Databricks own (built on top of Kubernetes) |
| Kubernetes-native infra | Kubernetes |
| Simple dedicated Spark cluster | Standalone |
| Local dev | Local mode (no cluster manager) |
| Glue | AWS manages it (hidden from you) |

## Key Things to Remember
### Cluster manager handles resource allocation — Spark handles task scheduling
- In Databricks or Glue — cluster manager is abstracted away, you don't configure it
- YARN = most battle-tested for big data workloads on Hadoop/EMR
- Kubernetes = future direction for cloud-native Spark



