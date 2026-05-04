
## Redshift Managed Storage (RMS)

## What is it?
- RMS is the storage layer used by RA3 nodes and Redshift Serverless
- Your data lives outside the compute node — in AWS-managed, S3-backed storage
- Compute and storage are completely decoupled

Analogy:

- DC2 = Your data is saved on your laptop's hard drive — tied to the machine
- RMS = Your data is saved on iCloud/Google Drive — the laptop can be changed, upgraded, or turned off, but data is always there

--- 
### How it Works

```
RA3 Compute Node
├── Local SSD Cache     ← hot/frequently accessed data lives here (fast)
└── RMS (S3-backed)     ← ALL data lives here permanently (scalable)

When query runs:
  Step 1 → Check local SSD cache first (fast path)
  Step 2 → If not in cache, fetch from RMS (slightly slower)
  Step 3 → Fetched data gets cached in SSD for next time
```

- Local SSD = just a cache, not permanent storage
- RMS = the actual source of truth for all your data
- Cache management is fully automatic — Redshift decides what stays hot

--- 

### Key Components
1. Local SSD Cache (on node)
- Holds recently or frequently accessed data blocks
- Fast — data reads from here are near-instant
- Limited in size — not all data fits in cache
- If node is replaced/resized → cache is rebuilt automatically from RMS
2. RMS Layer (S3-backed)
- Holds all your data permanently
- Scales to petabytes independently of compute
- Replicated across 3 AZs automatically — highly durable
- Managed entirely by AWS — you never interact with it directly

---
### Why it Matters
| Problem with DC2 | How RMS Solves it |
| :-- | :-- |
| Storage fills up → must add nodes | Storage scales independently |
| Adding nodes = paying for unwanted compute | Scale storage without touching compute |
| Node failure = risk of data loss | RMS is replicated across 3 AZs |
| Resize cluster = data redistribution (slow) | Resize is fast — data stays in RMS |

---
### RMS vs S3 — Are they the same?
- RMS -is backed by S3 but is NOT the same as your S3 buckets
- You cannot browse or access RMS directly from S3 console
- RMS is fully managed by Redshift internally
- Think of it as Redshift's private S3 — optimized for columnar block storage

```
Your S3 Bucket         → You own and manage it
RMS (internal S3)      → AWS manages it, you never see it directly
```

---
### Key Things to Remember

- RMS is only available with RA3 nodes and Serverless — DC2 does not use it
- Data in RMS is automatically encrypted at rest
- RMS storage is billed separately from compute (per GB per month)
- Even if you pause or resize the cluster — data in RMS is safe and intact
- Elastic Resize is much faster with RA3/RMS because data doesn't physically move
- RMS supports Data Sharing — multiple clusters can read same RMS data without copying

---
### Data Flow Summary


```
COPY from S3
      ↓
Data written to RMS (permanent home)
      ↓
Frequently queried blocks cached in Local SSD
      ↓
Query hits SSD cache → fast result
Query misses cache  → fetched from RMS → cached → fast next time
```

---
### Real-World Use Case
A company has 50TB of data in Redshift RA3
They want to upgrade compute from ra3.4xlarge to ra3.16xlarge for faster queries

Without RMS (DC2): Data physically stored on nodes → resize = redistribute 50TB → takes hours

With RMS: Data stays in RMS untouched → only compute nodes are swapped
→ Resize completes in minutes, zero data movement, zero downtime risk

After resize, new nodes start pulling hot data from RMS into their local SSD cache automatically

---

| Component | Used in Serverless? |
| :-- | :-- |
| DC2 Nodes | ❌ No |
| RA3 Nodes | ❌ Not explicitly — but concept is same |
| RMS (Managed Storage) | ✅ Yes — always |
| RPUs | ✅ Yes — this replaces node concept |
| AQUA | ✅ Yes — automatic |

### Why No Node Types in Serverless?

- In Provisioned Redshift → you pick node type → that determines compute + storage
- In Serverless → you don't pick nodes at all → AWS handles everything internally
- You only set Base RPU and Max RPU — that's your only compute control

```
Provisioned:
You pick → ra3.4xlarge × 4 nodes → you get compute + storage

Serverless:
You pick → Base: 8 RPU, Max: 64 RPU → AWS figures out the rest internally
``` 

### What Serverless Uses Internally

- AWS runs Serverless on RA3-like infrastructure internally — but you never see it
- Storage is always RMS-backed — same durability, same 3-AZ replication
-   AQUA acceleration is automatically applied where beneficial