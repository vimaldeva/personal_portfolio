## VACUUM

### What is it?
Redshift maintenance command that:
- Re-sorts unsorted rows added after initial load
- Reclaims disk space from deleted/updated rows (ghost rows)

Needed because Redshift uses immutable blocks — deletes don't free space immediately

```
After many INSERTs/DELETEs/UPDATEs:
├── Unsorted rows at bottom of table → Sort Key loses effectiveness
└── Ghost rows taking up disk space → wasted storage

VACUUM fixes both ✅
```

### VACUUM Types
| Type | What it Does | When to Use |
| :-- | :-- | :-- |
| VACUUM FULL | Re-sorts + reclaims space | Default, covers everything |
| VACUUM SORT ONLY | Re-sorts only, no space reclaim | When disk space isn't issue |
| VACUUM DELETE ONLY | Reclaims space only, no re-sort | After heavy deletes |
| VACUUM REINDEX | Rebuilds interleaved sort key index | Only for Interleaved Sort Keys |


``` VACUUM FULL orders;               -- full vacuum
VACUUM SORT ONLY orders;          -- re-sort only
VACUUM DELETE ONLY orders;        -- reclaim space only
VACUUM REINDEX orders;            -- interleaved sort key rebuild
```

----
### Key Things to Remember
- VACUUM runs online — table still queryable during vacuum
- Automatic Vacuum runs in background by default — but manual vacuum is faster
- VACUUM REINDEX is very expensive on large tables — plan carefully
- Check tables needing vacuum:
```
SELECT * FROM svv_vacuum_summary
ORDER BY estimated_optimal_rows DESC;
```
After large deletes → run VACUUM DELETE ONLY first (fastest space reclaim)