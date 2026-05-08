### Credits and Cost per Size

What is a Credit?
- Snowflake's unit of compute consumption
- 1 credit = a certain amount of compute power for 1 hour
- You buy credits → warehouses consume credits → you're billed

### Credits per Warehouse Size per Hour



| Size | Credits/Hour | Credits/Second |
| :-- | :-- | :-- |
| X-Small | 1 | 0.000278 |
| Small | 2 | 0.000556 |
| Medium | 4 | 0.001111 |
| Large | 8 | 0.002222 |
| X-Large | 16 | 0.004444 |
| 2X-Large | 32 | 0.008889 |
| 3X-Large | 64 | 0.017778 |
| 4X-Large | 128 | 0.035556 |


### Credit Cost (Approximate by Edition)
| Edition | Cost per Credit (USD approx) |
| :-- | :-- |
| Standard | ~$2.00 |
| Enterprise | ~$3.00 |
| Business Critical | ~$4.00 |

### What Consumes Credits?
| Resource | Credit Consumption |
| :-- | :-- |
| Virtual Warehouses | Per second while running |
| Snowpipe | Per file processed (serverless) |
| Automatic Clustering | Background reclustering |
| Search Optimization | Maintenance cost |
| Serverless Tasks | Per second of execution |
| Query Acceleration Service | Per second of QAS nodes |
| Materialized View maintenance | Background refresh |
| Cloud Services | If exceeds 10% of daily compute |

### Storage Costs (Separate from Credits)
| Storage Type | Billed At |
| :-- | :-- |
| Active data | Per TB per month |
| Time Travel data | Per TB per month |
| Fail-safe data | Per TB per month (included) |

```
Reducing storage cost tips:
- Reduce Time Travel retention on large tables
- Use TRANSIENT tables (no Fail-safe, 0-1 day Time Travel)
- Run PURGE on old stage files
```

### Key Things to Remember
- Minimum billing = 60 seconds per warehouse start
- Multi-cluster: 3 clusters running = 3x credits consumed
- Storage and compute billed completely separately
- Credits consumed even if query returns zero rows — compute happened
- Use Resource Monitors to set credit budgets and alerts
```
-- Create resource monitor to alert at 80% and suspend at 100%
CREATE RESOURCE MONITOR monthly_limit
    WITH CREDIT_QUOTA = 500
    TRIGGERS
        ON 80 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND;

ALTER WAREHOUSE analytics_wh SET RESOURCE_MONITOR = monthly_limit;
```


