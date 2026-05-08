## Views

### Standard View
- Saved SQL query — no data stored, executes query on access
- Underlying query visible to all users who can access view

```
CREATE VIEW high_value_orders AS
SELECT * FROM orders WHERE revenue > 10000;
```
### Secure View ✅
- Same as standard view but underlying SQL is hidden from non-owners
- Query definition not visible via SHOW VIEWS or GET_DDL
- Good for: sharing data without exposing business logic

```
CREATE SECURE VIEW customer_summary AS
SELECT customer_id, SUM(revenue) as total
FROM orders
GROUP BY customer_id;
```

### Materialized View
- Pre-computed, stored result — data physically stored like a table
- Automatically refreshed by Snowflake in background
- Faster than standard view — no recompute on every query

```
CREATE MATERIALIZED VIEW daily_revenue AS
SELECT order_date, SUM(revenue) as total
FROM orders
GROUP BY order_date;
```

| Feature | Standard | Secure | Materialized |
| :-- | :-- | :-- | :-- |
| Data stored | ❌ | ❌ | ✅ |
| SQL hidden | ❌ | ✅ | ❌ |
| Auto-refresh | N/A | N/A | ✅ |
| Query speed | Base table speed | Base table speed | Fast (pre-computed) |
| Maintenance cost | None | None | Background credits |


### Key Things to Remember
- Materialized Views only support limited SQL — no joins across multiple base tables, no UDFs
- Secure Views disable some optimizations — slightly slower than standard views
- Use Materialized Views for expensive aggregations queried frequently
- Materialized View refresh is automatic but adds background compute cost