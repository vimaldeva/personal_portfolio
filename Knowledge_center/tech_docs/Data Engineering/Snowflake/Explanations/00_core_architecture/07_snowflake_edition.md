## Snowflake Editions

### Overview

```
Standard → Enterprise → Business Critical → Virtual Private Snowflake (VPS)
(basic)     (most common)  (regulated industries)  (maximum isolation)
```

| Feature | Standard | Enterprise | Business Critical | VPS |
| :-- | :-- | :-- | :-- | :-- |
| All basic SQL features | ✅ | ✅ | ✅ | ✅ |
| Multi-cluster warehouses | ❌ | ✅ | ✅ | ✅ |
| Time Travel (max days) | 1 day | 90 days | 90 days | 90 days |
| Database replication | ❌ | ✅ | ✅ | ✅ |
| Column-level security | ❌ | ✅ | ✅ | ✅ |
| Row-level security | ❌ | ✅ | ✅ | ✅ |
| Dynamic Data Masking | ❌ | ✅ | ✅ | ✅ |
| HIPAA / PCI compliance | ❌ | ❌ | ✅ | ✅ |
| Tri-Secret Secure (CMK) | ❌ | ❌ | ✅ | ✅ |
| AWS PrivateLink | ❌ | ❌ | ✅ | ✅ |
| Dedicated VPC (full isolation) | ❌ | ❌ | ❌ | ✅ |
| Separate metadata store | ❌ | ❌ | ❌ | ✅ |


---
### Standard
- Entry-level — basic data warehousing
- 1 day Time Travel only
- No governance features (masking, row policies)
- Good for: startups, non-sensitive workloads, learning

### Enterprise ✅ (Most Common)
- All Standard features +
- 90-day Time Travel
- Multi-cluster warehouses for concurrency
- Column + Row-level security
- Dynamic Data Masking
- Good for: most production enterprise workloads

### Business Critical
- All Enterprise features +
- HIPAA, PCI-DSS, SOC 2 Type II compliance
- Tri-Secret Secure — customer-managed encryption keys
- AWS PrivateLink / Azure Private Link — no public internet
- Database Failover/Failback for disaster recovery
- Good for: healthcare, finance, regulated industries

### VPS (Virtual Private Snowflake)
- All Business Critical features +
- Completely dedicated Snowflake environment — no shared infrastructure
- Separate metadata store — fully isolated
- Highest security, highest cost
- Good for: government, defense, ultra-sensitive workloads