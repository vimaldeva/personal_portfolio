## Workload Isolation

### What is it?
- Keeping different workloads completely separate so they don't compete for resources
- Goes beyond WLM queues — full resource isolation between environments/teams

### Ways to Achieve Workload Isolation in Redshift

#### Option 1 — WLM Queues (Basic Isolation)
- Separate queues with fixed memory % per team/workload
- Still on same cluster — not true isolation

#### Option 2 — Redshift Data Sharing (True Isolation) ✅
- Producer cluster owns and stores data
- Consumer cluster queries data without storing it
- Each cluster has completely separate compute

```
Producer Cluster (ETL writes here)
        ↓ Data Sharing
Consumer Cluster 1 (BI team queries here)
Consumer Cluster 2 (Data Science queries here)

ETL heavy loads → don't affect BI queries ✅
```

```
Producer Cluster (ETL writes here)
        ↓ Data Sharing
Consumer Cluster 1 (BI team queries here)
Consumer Cluster 2 (Data Science queries here)

ETL heavy loads → don't affect BI queries ✅
```

### Option 3 — Redshift Serverless Workgroups
- Separate workgroups per team → completely isolated compute
- Each workgroup scales independently


### Key Things to Remember
- WLM queues = soft isolation — same cluster, shared resources
- Data Sharing = hard isolation — separate clusters, no resource contention
- Data Sharing requires RA3 nodes — not available on DC2
- Consumer clusters read data live from producer — no data copy/duplication
- Workload isolation via Data Sharing adds no extra storage cost