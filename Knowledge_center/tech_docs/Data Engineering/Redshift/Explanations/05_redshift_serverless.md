## Redshift Serverless

### What is it?
- Redshift without managing clusters — no nodes, no sizing, no manual scaling
- You just run queries — AWS automatically provisions and scales compute behind the scenes
- Pay only for compute used during query execution (not idle time)

Analogy:
- Provisioned Redshift = Owning a car — you pay insurance, maintenance 24/7 even when parked
- Redshift Serverless = Uber — you pay only when you're actually riding

---
### Core Concepts
#### Namespace
- A logical container that holds your databases, schemas, tables, users
- Stores your actual data (linked to RMS — RA3 managed storage)
- Think of it as: "where your data lives"

#### Workgroup
- A compute configuration attached to a namespace
- Defines how much compute power is available for queries
- Think of it as: "how much power to use when running queries"

```
Namespace (data + metadata)
    └── Workgroup (compute config)
            └── Runs your queries
```

- One namespace can have one workgroup
- You can have multiple namespaces for different environments (dev, prod)

---
### How it Works

```
You submit a query
        ↓
Redshift Serverless checks if compute is warm
        ↓
Auto-provisions compute (RPUs) needed
        ↓
Runs query → returns result
        ↓
Scales back down when idle
```

---
### RPU — Redshift Processing Units

- The unit of compute in Serverless (like DPU in Glue)
- 1 RPU = certain amount of CPU + RAM
- You set a Base RPU (minimum) and Max RPU (ceiling)
- Serverless auto-scales between base and max based on query load

```
Base RPU: 8   → always warm, ready to query
Max RPU:  128 → can scale up to this during heavy load
```

| RPU Setting | Impact |
| :-- | :-- |
| Higher Base RPU | Faster response, higher minimum cost |
| Higher Max RPU | Handles bigger queries, costs more at peak |
| Lower Max RPU | Cost controlled but may throttle heavy queries |

---
### Serverless vs. Provisioned — When to Use What?

| Factor | Serverless | Provisioned |
| :-- | :-- | :-- |
| Cluster management | ❌ Not needed | ✅ You manage |
| Unpredictable/sporadic workloads | ✅ Best fit | ❌ Wasteful |
| Constant heavy workloads | ❌ Can get expensive | ✅ More cost-efficient |
| Auto-scaling | ✅ Automatic | ⚠️ Manual or limited |
| Pricing | Per RPU-second used | Per node-hour |
| Startup/warm-up time | Small delay possible | Always running |
| Fine-grained cost control | ⚠️ Harder to predict | ✅ Predictable |

---
### Key Things to Remember

- No cluster to create — just create a namespace + workgroup
- Data is stored in RA3-backed managed storage (same as RA3 provisioned)
- Supports same SQL, same drivers, same integrations as provisioned Redshift
- Cold start — if cluster has been idle, first query may take a few seconds longer
- You can set a usage limit to cap costs (alerts or stop queries when limit hit)
- Supports Data Sharing, Spectrum, Federated Queries — same as provisioned
- Not ideal for consistently heavy 24/7 workloads — provisioned is cheaper there

--- 

### Pricing Model

```
Cost = RPU-seconds consumed × price per RPU-second
     + Storage cost (per GB per month)

Example:
Query takes 10 seconds on 8 RPUs
= 80 RPU-seconds × $0.000463
= ~$0.037 per query
```

---
### Real-World Use Case

A data team runs ad-hoc reports — sometimes 5 queries a day, sometimes 200

With provisioned cluster → paying for nodes 24/7 even at 2AM when nobody queries

With Serverless:

Base RPU: 8 (stays warm during business hours)
Max RPU: 64 (scales up when analysts run heavy reports)
Nights/weekends → scales to 0 → no compute cost
Team pays only for what they actually use → significant cost savings