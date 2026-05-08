## Core Architecture
- Shared Disk vs Shared Nothing vs Snowflake's Hybrid Architecture
- Three Layer Architecture (Storage, Compute, Cloud Services)
- Virtual Warehouses
- Micro-partitions
- Columnar Storage
- Metadata Layer
- Cloud Platform Support (AWS, Azure, GCP)
- Snowflake Editions (Standard, Enterprise, Business Critical, VPS)

---
## Virtual Warehouses (Compute)
What is a Virtual Warehouse
Warehouse Sizes (XS to 6XL)
Multi-cluster Warehouses
Auto-suspend and Auto-resume
Warehouse Scaling Policies (Economy vs Standard)
Query Acceleration Service (QAS)
Concurrency and Queuing
Credits and Cost per Size
Warehouse Monitoring

---
## Storage & Micro-partitions
Micro-partition Structure
Automatic Clustering
Clustering Keys
Clustering Depth
Reclustering
Automatic vs Manual Reclustering
Search Optimization Service
Data Pruning via Micro-partitions
Zone Maps in Snowflake

--- 
## Database Objects
Databases
Schemas
Tables (Permanent, Temporary, Transient, External)
Views (Standard, Secure, Materialized)
Sequences
Stages (Internal vs External)
File Formats
Pipes (Snowpipe)
Streams
Tasks
Procedures
Functions (UDFs, UDTFs)
Alerts
Dynamic Tables

--- 
## Data Loading & Ingestion
COPY INTO Command
Stages (User, Table, Named)
Internal Stages vs External Stages (S3, Azure Blob, GCS)
File Formats (CSV, JSON, Parquet, Avro, ORC)
PUT Command (upload to internal stage)
GET Command (download from internal stage)
Snowpipe (continuous ingestion)
Snowpipe Streaming
Auto-Ingest with SQS (S3 events)
COPY Options (ON_ERROR, PURGE, FORCE)
Validation Mode
Load History

---
## Data Unloading
COPY INTO (location) — unload to S3/Azure/GCS
Unload to Internal Stage
GET command to download
File format options for unload
Partition by column during unload

--- 
## Querying & SQL
Snowflake SQL Dialect
Semi-structured Data Queries (VARIANT, OBJECT, ARRAY)
FLATTEN function
LATERAL FLATTEN
Dot notation and bracket notation for JSON
Window Functions
Conditional Expressions (IFF, DECODE, CASE)
QUALIFY clause
PIVOT and UNPIVOT
ASOF JOIN
MATCH_CONDITION joins
Recursive CTEs
SAMPLE / TABLESAMPLE
Result Set Caching
Query Profile

---
## Semi-Structured Data
VARIANT Data Type
OBJECT Data Type
ARRAY Data Type
PARSE_JSON
TO_VARIANT, TO_OBJECT, TO_ARRAY
Querying nested JSON
FLATTEN + LATERAL
STRIP_OUTER_ARRAY
Semi-structured indexing
Schema detection (INFER_SCHEMA)

---
## Time Travel & Fail-safe
Time Travel (AT, BEFORE clause)
Time Travel retention period (0-90 days per edition)
Querying historical data
Restoring dropped tables/schemas/databases
UNDROP command
Fail-safe (7-day additional protection)
Time Travel vs Fail-safe
Storage costs for Time Travel

---
## Cloning
Zero-copy Cloning
Cloning Tables, Schemas, Databases
Cloning Streams and Tasks
Clone + Time Travel (clone at a point in time)
Dev/Test environment patterns using cloning
Storage implications of cloning

---
## Data Sharing
Secure Data Sharing
Provider and Consumer accounts
Shares object
Reader Accounts
Data Exchange
Snowflake Marketplace
Cross-region and Cross-cloud sharing (Replication)
Private Data Exchange
Listing types (Public, Private)

---
## Streams & Tasks (CDC Pipeline)
Streams — What they are
Stream Types (Standard, Append-only, Insert-only)
Stream columns (METADATAACTION, METADATA, ISUPDATE, METADATA$ROW_ID)
Stream offset and staleness
Tasks — What they are
Standalone Tasks vs DAG of Tasks
Task Scheduling (CRON vs interval)
Task predecessors (dependencies)
Serverless Tasks vs Warehouse Tasks
Task history and monitoring
Combining Streams + Tasks for CDC pipelines

---
## Dynamic Tables
What are Dynamic Tables
Dynamic Tables vs Materialized Views vs Streams+Tasks
Target Lag
Refresh modes (Incremental vs Full)
Dynamic Table pipelines (chaining)
Monitoring Dynamic Tables

---
## Snowpipe & Continuous Ingestion
Snowpipe vs COPY INTO
Auto-ingest (event-based — S3 SQS, Azure Event Grid)
REST API-based Snowpipe
Snowpipe Streaming (SDK-based, row-level)
Pipe status and load history
Error handling in Snowpipe
REFRESH Pipe

---
## Performance & Optimization
Result Cache
Metadata Cache
Warehouse Cache (local SSD)
Query Profile (reading and interpreting)
Partition Pruning
Clustering Keys (when and how to choose)
Search Optimization Service
Materialized Views for performance
Query Acceleration Service (QAS)
Spilling to disk (local vs remote)
Exploding joins
JOIN order optimization

---
## Security & Access Control
RBAC (Role-Based Access Control)
DAC (Discretionary Access Control)
System Roles (ACCOUNTADMIN, SYSADMIN, SECURITYADMIN, USERADMIN, PUBLIC)
Custom Roles and Role Hierarchy
Privileges (GRANT, REVOKE)
Object ownership
Column-Level Security (Column Masking Policies)
Row-Level Security (Row Access Policies)
Dynamic Data Masking
Network Policies
MFA (Multi-Factor Authentication)
SSO / SAML Integration
OAuth
Key Pair Authentication
Private Link (AWS PrivateLink, Azure Private Link)
Tri-Secret Secure
Customer Managed Keys (CMK)

---
## Data Governance
Snowflake Horizon (governance suite)
Object Tagging
Tag-based Masking Policies
Data Classification
Access History
Object Dependencies
Sensitive Data Discovery
Lineage Tracking
Trust Center

--- 
## Replication & Business Continuity
Database Replication
Account Replication
Replication Groups
Failover and Failback
Cross-region Replication
Cross-cloud Replication
Business Continuity (RPO, RTO)

---
## Snowpark
What is Snowpark
Snowpark vs PySpark
Snowpark DataFrames
Lazy Evaluation in Snowpark
Snowpark Python, Java, Scala
UDFs in Snowpark
UDTFs (User Defined Table Functions)
Stored Procedures in Snowpark
Snowpark ML
Snowpark for Python Libraries (pandas on Snowpark)

---
## Snowflake Connectors & Integrations
Python Connector
JDBC / ODBC Connectors
Spark Connector
dbt + Snowflake
Kafka Connector
Airflow + Snowflake
AWS Glue + Snowflake
BI Tools (Tableau, PowerBI, QuickSight)
Fivetran / Airbyte integration
Snowflake Native Apps

---
## Cost Management
Credit-based pricing model
Storage costs (active vs time travel vs fail-safe)
Compute vs Storage billing separation
Resource Monitors
Credit usage by warehouse
Auto-suspend best practices
Serverless feature costs (Snowpipe, Tasks, Search Optimization)
Cost visibility queries (ACCOUNT_USAGE schema)

---
Account Usage & Monitoring
INFORMATION_SCHEMA (per database, short retention)
ACCOUNT_USAGE schema (org-level, longer retention)
Key views:
- QUERY_HISTORY
- WAREHOUSE_METERING_HISTORY
- LOGIN_HISTORY
- ACCESS_HISTORY
- COPY_HISTORY
- PIPE_USAGE_HISTORY
- TABLE_STORAGE_METRICS
- TASK_HISTORY
- STREAM_USAGE_HISTORY

---
## Scenarios You Must Know How to Handle
#### Loading & Ingestion

How to load JSON with nested arrays into a Snowflake table
How to handle load errors using VALIDATION_MODE before actual load
How to set up auto-ingest Snowpipe from S3
How to reload/reprocess files already loaded (FORCE=TRUE)
How to load only new files without reloading old ones

#### Semi-Structured Data

How to flatten deeply nested JSON into rows
How to query a specific key inside a VARIANT column
How to detect and infer schema from Parquet/JSON files

#### Performance

How to fix a slow query using Query Profile
How to reduce credit consumption for sporadic workloads
How to set up Clustering Keys for a large table
How to handle warehouse spilling to disk
How to use Result Cache to avoid redundant compute

#### CDC & Pipelines

How to build a full CDC pipeline using Streams + Tasks
How to detect INSERT vs UPDATE vs DELETE using stream metadata columns
How to build incremental pipelines using Dynamic Tables
How to chain Tasks into a DAG for dependency-based execution

#### Time Travel & Recovery

How to recover an accidentally dropped table
How to query data as it existed 3 days ago
How to clone production DB to create a dev environment
How to clone a table at a specific point in time

#### Security & Governance

How to mask PII columns for non-admin roles
How to restrict rows based on a user's department (Row Access Policy)
How to audit who accessed what data and when
How to prevent data exfiltration using network policies

#### Data Sharing

How to share live data with an external company without copying it
How to set up cross-region data sharing
How to create a Reader Account for consumers without Snowflake accounts

#### Cost Control

How to set up Resource Monitors to prevent credit overruns
How to identify the most expensive queries in the account
How to right-size warehouse for a given workload
How to reduce Time Travel storage costs on large tables