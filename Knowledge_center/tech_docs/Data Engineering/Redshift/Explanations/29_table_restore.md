## Table Restores (Snapshot Isolation)

### What is it?
- Snapshots
- Point-in-time backups of your entire Redshift cluster
- Stored in S3 automatically — managed by AWS
- Used to restore entire cluster or individual tables

Snapshot Types

| Type | How it Works |
| :-- | :-- |
| Automated | Taken every 8 hours automatically, retained 1-35 days |
| Manual | You trigger it, retained until you delete it |

```
-- Create manual snapshot
CREATE SNAPSHOT my_snapshot OF CLUSTER my-cluster;

-- Restore single table from snapshot (without full cluster restore)
RESTORE TABLE orders
FROM CLUSTER SNAPSHOT my_snapshot
NAMESPACE 'target_namespace'
TARGET TABLE orders_restored;
```

### Snapshot Isolation
- Redshift uses snapshot isolation for transactions
- When a query starts → it sees a consistent snapshot of data at that moment
- Other transactions committing during your query don't affect your results

```
Transaction A starts → sees snapshot at T1
Transaction B commits new rows at T2
Transaction A query still sees T1 snapshot → consistent results ✅
```

### Key Things to Remember
- Automated snapshots are free (stored in S3 managed by Redshift)
- Manual snapshots stored until explicitly deleted — you pay S3 storage
- Can restore a single table without restoring entire cluster
- Cross-region snapshot copy available for disaster recovery
- Snapshot isolation ensures no dirty reads — queries always see consistent data
- Restored table comes back as a new table — original table untouched