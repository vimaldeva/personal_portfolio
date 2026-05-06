## Query Editor v2

### What is it?
- Web-based SQL editor for Redshift built into AWS Console
- No need for external tools like DBeaver or SQL Workbench
- Supports multiple clusters, serverless, and saved queries

### Key Features
- Schema browser — explore databases, tables, columns visually
- Query history — see past queries and results
- Notebooks — mix SQL + markdown (like Jupyter for Redshift)
- Collaboration — share saved queries with team
- Chart visualizations — basic charts directly from query results

### Key Things to Remember
- Requires IAM permissions to access (redshift:GetClusterCredentials)
- Queries run as specific DB user — permissions apply normally
- Good for ad-hoc querying and exploration — not for production pipelines
- Supports multi-statement execution in notebooks

