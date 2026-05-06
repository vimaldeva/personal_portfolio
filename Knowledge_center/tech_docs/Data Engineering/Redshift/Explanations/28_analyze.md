## ANALYZE

### What is it?
- Collects table statistics (row count, column distribution, data range) and stores them
- Redshift query optimizer uses these stats to build efficient query plans
- Stale stats → optimizer makes bad decisions → slow queries

```
Without fresh stats:
 Optimizer guesses table has 1000 rows → plans hash join
 Actual table has 1 billion rows → wrong plan → slow query ❌

With fresh stats:
Optimizer knows actual row count → picks correct join strategy ✅
```

#### Usage

```

ANALYZE orders;                    -- analyze full table
ANALYZE orders(order_date, revenue); -- analyze specific columns only
```

### Key Things to Remember
- Runs automatically after COPY command by default (STATUPDATE ON)
- Run manually after large bulk inserts or schema changes
- Lightweight compared to VACUUM — runs fast
- Check stale stats:
```

SELECT * FROM svv_table_info
WHERE stats_off > 10;   -- tables with >10% stale stats
```
stats_off = 0 → fully up to date, stats_off = 100 → completely stale
