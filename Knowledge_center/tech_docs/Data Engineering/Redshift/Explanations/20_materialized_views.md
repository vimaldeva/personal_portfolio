## Materialized Views

### What is it?
- A pre-computed, stored result of a query
- Instead of running expensive query every time → result is stored and reused
- Must be refreshed to reflect latest data

Analogy:

Regular View = asking chef to cook every time you order
Materialized View = chef cooks in advance, stores it → you just reheat
Refresh = cooking a fresh batch

#### Manual vs Auto-Refresh

| Type | How it refreshes |
| :-- | :-- |
| Manual | You run REFRESH MATERIALIZED VIEW explicitly |
| Auto | Redshift automatically refreshes when base data changes |

```
-- Create Materialized View
CREATE MATERIALIZED VIEW daily_sales AS
SELECT order_date, SUM(revenue) as total
FROM orders
GROUP BY order_date;

-- Manual Refresh
REFRESH MATERIALIZED VIEW daily_sales;

-- Auto Refresh
CREATE MATERIALIZED VIEW daily_sales
AUTO REFRESH YES
AS
SELECT order_date, SUM(revenue)
FROM orders
GROUP BY order_date;
```

### Key Things to Remember

- Auto-refresh happens asynchronously — slight delay after base table changes
- Materialized Views can be built on top of Spectrum external tables too
- Redshift can use MV for query rewriting — automatically uses MV even if query hits base table
- Use for expensive, frequently run aggregation queries
- Auto-refresh adds background compute cost — use wisely on large MVs

---

#### How These 3 Work Together — Real-World Use Case
Company has:

- Historical orders (3 years) in S3 → too large for Redshift → use Spectrum
- Live customer data in Aurora RDS → use Federated Query to enrich
- Daily sales dashboard hitting same aggregation query 100x/day → use Materialized View