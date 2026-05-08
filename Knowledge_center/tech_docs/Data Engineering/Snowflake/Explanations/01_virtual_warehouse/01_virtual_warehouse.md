## Virtual Warehouse

- A named cluster of compute resources (CPU + RAM + local SSD) that executes SQL queries
- Completely separate from storage — just the engine that processes data
- Can be started, stopped, resized without affecting data

### How a Warehouse Executes a Query

```
Query submitted to Warehouse
        ↓
Check local SSD cache first
        ↓ (cache miss)
Fetch relevant micro-partitions from Storage (S3)
        ↓
Cache fetched data in local SSD (for next time)
        ↓
Process data across all nodes in parallel
        ↓
Return result → also stored in Result Cache (Cloud Services)
```


- Each warehouse = completely isolated — no resource sharing between warehouses
- Multiple warehouses can read same table simultaneously — no locking
- Warehouse has its own local SSD cache — cache lost on suspend
- Billed in credits per second (minimum 60 seconds per start)

```
-- Create warehouse
CREATE WAREHOUSE analytics_wh
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    COMMENT = 'Used by BI team';

-- Use a warehouse
USE WAREHOUSE analytics_wh;

-- Manually suspend / resume
ALTER WAREHOUSE analytics_wh SUSPEND;
ALTER WAREHOUSE analytics_wh RESUME;

-- Resize on the fly
ALTER WAREHOUSE analytics_wh SET WAREHOUSE_SIZE = 'LARGE';
```