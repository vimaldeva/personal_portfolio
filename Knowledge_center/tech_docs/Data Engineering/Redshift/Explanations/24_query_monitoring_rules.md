## Query Monitoring Rules (QMR)

What is it?
- Rules that monitor running queries and take automatic action when thresholds are breached
- Prevents runaway queries from consuming all resources

```
Rule: IF query runs > 5 minutes AND scans > 1TB
      THEN → hop to next queue OR abort query
```

### Setup (Manual WLM)

```
"rules": [
  {
    "rule_name": "abort_long_queries",
    "predicate": [
      {"metric_name": "query_execution_time", "operator": ">", "value": 300},
      {"metric_name": "scan_row_count", "operator": ">", "value": 1000000000}
    ],
    "action": "abort"
  }
]
```

### Available Metrics for Rules
| Metric | What it Tracks |
| :-- | :-- |
| query_execution_time | How long query has run (seconds) |
| scan_row_count | Rows scanned |
| return_row_count | Rows returned to user |
| query_cpu_time | CPU consumed |
| query_blocks_read | Disk blocks read |

### Available Actions

| Action | What Happens |
| :-- | :-- |
| log | Log the query — no interruption |
| hop | Move query to next WLM queue |
| abort | Kill the query |


### Key Things to Remember
- QMR is part of Manual WLM — Automatic WLM has simplified version
- Use log first to understand patterns before using abort
- Good for catching accidental full table scans or missing WHERE clauses