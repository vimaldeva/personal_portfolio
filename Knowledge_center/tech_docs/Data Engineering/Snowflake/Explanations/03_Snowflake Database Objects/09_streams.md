## Streams

### What is it?
- A change tracking object on a table — captures INSERT, UPDATE, DELETE since last consumed
- Powers CDC (Change Data Capture) pipelines in Snowflake

```
-- Create stream on a table
CREATE STREAM orders_stream ON TABLE orders;

-- Query stream — see what changed
SELECT * FROM orders_stream;

-- Stream metadata columns:
-- METADATA$ACTION    → INSERT or DELETE
-- METADATA$ISUPDATE  → TRUE if this is part of an UPDATE
-- METADATA$ROW_ID    → unique row identifier
```

### How Changes Appear in Stream


```
Original row updated:
orders_stream shows:
┌──────────┬─────────────────┬──────────────────┐
│ order_id │ METADATA$ACTION │ METADATA$ISUPDATE│
├──────────┼─────────────────┼──────────────────┤
│ 101      │ DELETE          │ TRUE             │  ← old version
│ 101      │ INSERT          │ TRUE             │  ← new version
└──────────┴─────────────────┴──────────────────┘
```

### Stream Types
| Type | Captures |
| :-- | :-- |
| Standard | INSERT, UPDATE, DELETE |
| Append-only | INSERT only (faster, less overhead) |
| Insert-only | INSERT only — for external tables |


### Key Things to Remember

- Stream has an offset — marks last consumed position
- Consuming stream (in a DML + transaction) advances the offset
- Stream becomes stale if not consumed within data retention period
- Stream does not store data — reads from table's change tracking metadata



