## Result Caching

### What is it?
- Redshift caches query results in memory on the Leader Node
- Identical query run again → returns cached result instantly without re-executing
- Zero compute cost for cached queries

```
First run:   Query executes fully → result stored in cache
Second run:  Same query → Leader Node returns cache → no cluster compute used
```

### When Cache is Used vs Skipped

| Scenario | Cache Used? |
| :-- | :-- |
| Exact same query, same user | ✅ Yes |
| Same query, different user | ✅ Yes (if permissions same) |
| Underlying table data changed | ❌ No — re-executes |
| Query uses GETDATE() or random functions | ❌ No — result changes each time |
| User has different permissions on table | ❌ No |


### Key Things to Remember
- Enabled by default — no setup needed
- Cache is stored on Leader Node memory — limited size
- Disable for a session if you always need fresh results:
```


SET enable_result_cache_for_session TO OFF;
Great for dashboards that run same queries repeatedly

```