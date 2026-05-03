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



