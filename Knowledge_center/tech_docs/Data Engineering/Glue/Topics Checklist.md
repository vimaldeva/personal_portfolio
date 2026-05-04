### Glue

- Glue ETL jobs
- Glue database/ tables
- Glue data catalog
- Glue triggers (Scheduled, On-demand, Event-based)
- Glue workflow
- Glue studio (Visual ETL)
- Glue Databrew
- Glue crawlers
- Glue data quality

---
#### Other topics

- Recipies (databrew)
- Glue Databrew vs Glue ETL (when to select them)
- How Glue connects to other AWS services
- Glue architecture and frameworks (tell list of glue features eg.crawlers)
- Dynamic Frame
- Backward compatibility
- Forward compatibility
- Dynamic Frame vs Glue Dataframe

- Glue job configurations
- Configuration parameters
- Glue Bookmarks
- Limitations of Glue bookmark
- Security in Glue (IAM + lakeformation)
- Lakeformation
- Long running jobs, How to fix it
- Sample ETL script
- Job.commit
- VPC

---
#### Scenarios
- Will you sugggesst Glue for real time data processing
- Optimize performance of ETL jobs while dealing with large datasets.
- Optimixe Glue jobs for milllions of small files
- How Glue catalog is better that traditional database catalog

--- 
#### Others
- GlueContext
- Worker Types (Standard, G.1X, G.2X, G.4X, G.8X, G.025X)
- DPU (Data Processing Unit)
- Transformation APIs (ApplyMapping, Relationalize, Unnest, ResolveChoice)
- Auto Scaling
- Max Retries
- Timeout Settings
- CloudWatch Metrics (CPU Load, Memory Usage, Data Shuffle)
- Glue Data Quality (DQDL - Data Quality Definition Language)
- Glue Sensitive Data Detection (PII)

--- 
#### Advanced scenarios

How to handle Schema Drift when source columns change.
How to handle Nested JSON structures and flatten them for Relational databases.
How to handle Duplicate Records during the ETL process.
How to handle Mixed Data Types in a single column (e.g., String and Integer).

How to handle OOM (Out of Memory) errors in Spark jobs.
How to handle Slow Crawlers scanning millions of files in S3.
How to handle Small Files to improve downstream query performance (Athena/Redshift).
How to handle Data Skew where one worker is doing more work than others.

How to handle Incremental Data Loads using Job Bookmarks.
How to handle Reprocessing a specific time range of data.
How to handle Late Arriving Data in a partitioned S3 bucket.

How to handle Connecting to an On-Premise Database via VPN/Direct Connect.
How to handle Connection Timeouts when Glue cannot reach a VPC resource.
How to handle Cross-Account S3 Access where the bucket belongs to a different AWS account.
How to handle PII Data masking before saving to a Data Lake.

How to handle Job Dependencies (Job B starts only if Job A succeeds).
How to handle Failed Job Retries without duplicating data.
How to handle Cost Spikes by implementing Glue Flex or Auto Scaling.
How to handle Data Validation failures using Glue Data Quality rules.

---

### DPU

- DPU is the unit of compute power in AWS Glue
``` 1 DPU = 4 vCPUs + 16 GB RAM ```

- Similar concept to RPU in Redshift Serverless — it's just how Glue measures and bills compute

Analogy:
Instead of saying "I need 8 CPUs and 32GB RAM"
Glue says "I need 2 DPUs" — it's just a packaged unit of compute

```
Glue Job
    ↓
You define number of DPUs (or max DPUs for auto-scaling)
    ↓
Glue spins up Spark cluster using those DPUs
    ↓
1 DPU becomes the Driver (like Leader Node)
Remaining DPUs become Executors (like Compute Nodes)
    ↓
Job finishes → cluster torn down → billing stops

```


| Worker Type | DPU per Worker | vCPU | RAM | Best For |
| :-- | :-- | :-- | :-- | :-- |
| Standard | 1 DPU | 4 vCPU | 16 GB | General workloads |
| G.1X | 1 DPU | 4 vCPU | 16 GB | Memory-optimized per worker |
| G.2X | 2 DPU | 8 vCPU | 32 GB | Heavy transforms, large datasets |
| G.4X | 4 DPU | 16 vCPU | 64 GB | Very large workloads |
| G.8X | 8 DPU | 32 vCPU | 128 GB | Extremely large workloads |
| G.025X | 0.25 DPU | 2 vCPU | 4 GB | Python Shell / small jobs |

### Pricing 

```
Cost = DPU-hours used × price per DPU-hour

Example:
Job runs for 10 minutes using 10 DPUs
= 10 DPUs × (10/60) hours
= 1.67 DPU-hours × ~$0.44
= ~$0.73 per job run
```

### Key Things to Remember
- More DPUs = more parallel executors = faster job (up to a point)
- Adding DPUs doesn't always help — small datasets won't benefit from 20 DPUs
- G.2X or higher → use when you hit OOM (Out of Memory) errors
- G.025X → only for Python Shell jobs — lightest and cheapest
- Minimum DPUs for a Spark job = 2 DPUs (1 driver + 1 executor)
- Use Auto Scaling for unpredictable or variable data volume jobs



