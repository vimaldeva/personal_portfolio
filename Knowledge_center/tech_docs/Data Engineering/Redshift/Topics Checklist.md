### Redshift

- Leader Node vs. Compute Nodes
- Node Slices
- RA3 Nodes (Managed Storage)
- DC2 Nodes (Dense Compute)
- AQUA (Advanced Query Accelerator)
- Redshift Serverless
- Redshift Managed Storage (RMS)

- Columnar Storage
- Data Blocks and Zone Maps
- Distribution Styles (AUTO, KEY, EVEN, ALL)
- Distribution Skew
- Sort Keys (Compound vs. Interleaved)

- COPY Command
- Manifest Files
- S3 Ingestion
- Streaming Ingestion (Kinesis Data Streams, MSK)
- Auto-copy from S3
- UNLOAD Command
- UPSERT Patterns (Staging Tables)
- STL_LOAD_ERRORS

- Redshift Spectrum (External Tables)
- Federated Queries (RDS, Aurora)
- Materialized Views (Manual vs. Auto-refresh)
- Query Plan / Explain Plan
- Workload Management (WLM - Automatic vs. Manual)
- Concurrency Scaling
- Query Monitoring Rules (QMR)
- Short Query Acceleration (SQA)
- Result Caching

- VACUUM (FULL, DELETE ONLY, SORT ONLY, REINDEX)
- ANALYZE Command
- Table Restores (Snapshot Isolation)
- Classic Resize vs. Elastic Resize
- Cross-Region Snapshot Copy
- Workload Isolation

- Database Groups, Users, and Roles
- Row-Level Security (RLS)
- Column-Level Security
- Dynamic Data Masking
- Query Editor v2
- Enhanced VPC Routing
- HSM (Hardware Security Module) Integration
- Redshift Data Sharing (Producer/Consumer clusters)

- Redshift ML (Integration with SageMaker)
- Lambda UDFs (User Defined Functions)
- Stored Procedures (PL/pgSQL)
- Redshift Data API

---
#### Scenarios

How to handle Query Queueing when multiple users run heavy reports simultaneously.
How to handle Data Skew where one slice is processing significantly more data than others.
How to handle Slow Joins between a very large fact table and a small dimension table.
How to handle Ghost Rows (deleted records) taking up disk space and slowing down scans.
How to handle Stale Statistics that cause the optimizer to choose inefficient query plans.

How to handle Large File Ingestion efficiently (Parallelism vs. Serial loading).
How to handle Upserts (Update or Insert) since Redshift doesn't have a native UPSERT command.
How to handle Data Format Mismatches during a COPY command from S3.
How to handle Cross-Database Queries within the same Redshift cluster.

How to handle Disk Full Errors on DC2 nodes without deleting data.
How to handle Scaling for Peak Hours without paying for high-spec nodes 24/7.
How to handle Cold Data that is rarely accessed but too large to keep in local storage.

How to handle Cross-Account Data Sharing without physically moving or copying data.
How to handle Access Control for specific rows based on a user's department.
How to handle Connecting to Redshift from a private subnet without an IGW (Internet Gateway).
How to handle Query Performance Degradation after a large data load or schema change.

How to handle Small Files in Spectrum causing slow external query performance.
How to handle Partition Pruning for external tables in S3.
How to handle Schema Evolution in S3 Parquet files queried via Spectrum.
How to handle Federated Queries joining Redshift data with RDS/Aurora data.
How to handle Materialized View Refreshes that take too long or lock the base tables.
How to handle Concurrency Scaling costs when many users run queries simultaneously.
How to handle Result Caching when the underlying data changes frequently.
How to handle Redshift ML model training and inference within the database.