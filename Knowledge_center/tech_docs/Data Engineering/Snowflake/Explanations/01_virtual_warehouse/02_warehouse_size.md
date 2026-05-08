## Warehouse Sizes (XS to 6XL)

| Size | Nodes | Credits/Hour | Credits/Second |
| :-- | :-- | :-- | :-- |
| X-Small (XS) | 1 | 1 | 0.0003 |
| Small (S) | 2 | 2 | 0.0006 |
| Medium (M) | 4 | 4 | 0.0011 |
| Large (L) | 8 | 8 | 0.0022 |
| X-Large (XL) | 16 | 16 | 0.0044 |
| 2X-Large (2XL) | 32 | 32 | 0.0089 |
| 3X-Large (3XL) | 64 | 64 | 0.0178 |
| 4X-Large (4XL) | 128 | 128 | 0.0356 |
| 5X-Large (5XL) | 256 | 256 | — |
| 6X-Large (6XL) | 512 | 512 | — |

- Credits double with each size up
- Nodes double with each size up
- 5XL and 6XL available in Enterprise edition and above

### Bigger Warehouse — Does it Always Help?


```
Scenario 1: Simple query on 1GB table
XS warehouse → 2 seconds
XL warehouse → 2 seconds  ← no improvement, data too small

Scenario 2: Complex query on 5TB table
XS warehouse → 45 minutes
XL warehouse → 3 minutes  ← massive improvement

Scenario 3: Many small concurrent queries
M warehouse → queries queue up
M warehouse (multi-cluster) → queries spread across clusters ✅
```

#### Rule of thumb:

- Bigger size → helps with query complexity and data volume (scale up)
- Multi-cluster → helps with concurrency (scale out)

### Choosing Right Size

```
Start with SMALL or MEDIUM
        ↓
Check Query Profile → is it slow?
        ↓
Is data large / query complex?  → Scale UP (bigger size)
Are many users queuing?         → Scale OUT (multi-cluster)
Is query hitting cache?         → No change needed
```
