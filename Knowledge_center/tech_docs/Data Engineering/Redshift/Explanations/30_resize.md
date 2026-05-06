## Classic Resize vs Elastic Resize

### What is it?
- Both are ways to change cluster size (add/remove nodes or change node type)
- They differ hugely in how long it takes and cluster availability during resize

### Elastic Resize ✅ (Preferred)
- Adds or removes nodes quickly (minutes)
- Cluster stays available during resize (brief connection drops only)
- Data stays in RMS — no physical data movement needed
- Limited to doubling or halving node count (some restrictions apply)

```
ra3.4xlarge × 2 nodes  →  ra3.4xlarge × 4 nodes
Done in ~5-10 minutes, cluster stays online ✅
```

### Classic Resize ⚠️ (Legacy)
- Can change both node type AND node count
- Cluster goes into read-only mode during resize — no writes allowed
- Takes hours — all data physically redistributed to new nodes
- Use only when Elastic Resize can't achieve what you need

```
dc2.large × 4 nodes  →  ra3.4xlarge × 8 nodes
Read-only for hours during migration ❌
```

### Comparison

| Factor | Elastic Resize | Classic Resize |
| :-- | :-- | :-- |
| Speed | Minutes | Hours |
| Cluster availability | ✅ Online (brief drop) | ❌ Read-only |
| Change node type | ❌ Limited | ✅ Any type |
| Change node count | ✅ Yes (with limits) | ✅ Yes |
| Data movement | ❌ None (RMS) | ✅ Full redistribution |

### Key Things to Remember
- Always try Elastic Resize first — faster and no downtime
- Classic Resize needed when switching node types (DC2 → RA3)
- Elastic Resize requires RA3 nodes — DC2 has more restrictions
- Schedule Classic Resize during maintenance window — cluster goes read-only



