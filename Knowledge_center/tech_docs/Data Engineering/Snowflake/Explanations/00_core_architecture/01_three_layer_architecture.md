## Three Layer Architecture

```
┌─────────────────────────────────────────┐
│         CLOUD SERVICES LAYER            │  ← Brain
│  Authentication, Optimization,          │
│  Metadata, Security, Query Parsing      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         COMPUTE LAYER                   │  ← Muscles
│  Virtual Warehouses (MPP clusters)      │
│  Local SSD Cache per warehouse          │
│  Executes queries, processes data       │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         STORAGE LAYER                   │  ← Memory
│  Data stored in micro-partitions        │
│  Columnar compressed format             │
│  On S3 / Azure Blob / GCS               │
│  Managed entirely by Snowflake          │
└─────────────────────────────────────────┘
```

### Layer 1 — Storage Layer
- All data stored as columnar compressed micro-partitions in cloud object storage (S3/Azure/GCS)
- You never interact with this directly — Snowflake manages it
- Storage billed separately from compute
- Data is encrypted at rest always
- Stores: table data, query results, Time Travel data, Fail-safe data

### Layer 2 — Compute Layer (Virtual Warehouses)
- MPP (Massively Parallel Processing) clusters that execute queries
- Each warehouse has local SSD disk cache — hot data cached here
- Multiple warehouses can run simultaneously on same data
- Warehouses don't share compute — completely isolated
- Auto-suspend when idle → no compute cost when not running
 ### Layer 3 — Cloud Services Layer
- The brain of Snowflake — always running (no suspend)
Handles:
    - Authentication — user login, MFA, SSO
    - Query parsing & optimization — builds execution plan
    - Metadata management — schema, table stats, micro-partition info
    - Transaction management — ACID compliance
    - Security — access control, encryption key management
- Billed at 10% of daily compute if exceeds free threshold
- This layer is why Snowflake needs zero administration — it manages itself

---

### Key Things to Remember
- Three layers are completely independent — scale each separately
- Cloud Services layer = always on — small cost even with warehouses suspended
- Multiple virtual warehouses = no resource contention — each fully isolated
- Same data readable by all warehouses simultaneously — no locking