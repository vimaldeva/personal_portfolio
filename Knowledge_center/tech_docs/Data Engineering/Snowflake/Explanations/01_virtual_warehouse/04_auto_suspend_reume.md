## Auto-Suspend and Auto-Resume

### Auto-Suspend
- Warehouse automatically shuts down after N seconds of inactivity
- No queries running → timer starts → warehouse suspends → billing stops
- Local SSD cache is lost on suspend

```
ALTER WAREHOUSE my_wh SET AUTO_SUSPEND = 300;  -- suspend after 5 mins idle
ALTER WAREHOUSE my_wh SET AUTO_SUSPEND = 60;   -- suspend after 1 min idle
ALTER WAREHOUSE my_wh SET AUTO_SUSPEND = 0;    -- never auto-suspend
```

### Auto-Resume
- Warehouse automatically starts when a query is submitted
- User submits query → warehouse resumes → query runs
- Transparent to users — small resume delay (few seconds)

```
ALTER WAREHOUSE my_wh SET AUTO_RESUME = TRUE;   -- auto-start on query
ALTER WAREHOUSE my_wh SET AUTO_RESUME = FALSE;  -- must manually resume
```

### Auto-Suspend Strategy by Use Case

| Use Case | Recommended Auto-Suspend |
| :-- | :-- |
| Interactive BI dashboards | 300-600 seconds (5-10 mins) |
| Scheduled ETL jobs | 60 seconds (job finishes, suspend fast) |
| Dev/Test warehouses | 60 seconds |
| Always-on production | 600+ seconds or disable suspend |
| Overnight batch jobs | 60-120 seconds |

### Minimum Billing — Important!

```
Warehouse starts → runs for 15 seconds → suspended
→ Still billed for MINIMUM 60 SECONDS ⚠️

Warehouse starts → runs for 90 seconds → suspended
→ Billed for exactly 90 seconds ✅

Warehouse resumes → runs → resumes again within 60 seconds
→ Each resume = new 60-second minimum
```

- Avoid rapid start/stop cycles — each resume costs minimum 60 seconds
- If warehouse suspends and resumes frequently → consider higher auto-suspend time

### Key Things to Remember
- AUTO_RESUME = TRUE is default and recommended — never blocks users
- AUTO_SUSPEND = 0 means never suspend — warehouse runs 24/7 → expensive
- Cache is cold after resume — first queries post-resume are slower
- Auto-suspend timer resets on every query submission

