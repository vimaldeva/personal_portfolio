## Validation Mode

### What is it?
- Dry-run COPY — validates files without actually loading data
- Catches errors before you commit to loading
- No warehouse credits consumed for data loading — just parsing

```
-- Validate — returns errors without loading
COPY INTO orders
FROM @my_stage
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1)
VALIDATION_MODE = 'RETURN_ERRORS';      -- show all errors

-- Return first N rows that would be loaded (preview)
COPY INTO orders
FROM @my_stage
VALIDATION_MODE = 'RETURN_10_ROWS';    -- preview first 10 rows

-- Return all rows that would be loaded
COPY INTO orders
FROM @my_stage
VALIDATION_MODE = 'RETURN_ALL_ERRORS'; -- comprehensive error report
```

### Sample Error Output

```
┌────────────┬─────────────────────────────────────────────────┐
│ ERROR      │ Numeric value 'abc' is not recognized           │
│ FILE       │ orders_jan.csv                                  │
│ LINE       │ 145                                             │
│ CHARACTER  │ 3                                               │
│ COLUMN     │ REVENUE                                         │
└────────────┴─────────────────────────────────────────────────┘
```

### Key Things to Remember
- Always run VALIDATION_MODE before loading new file formats or first-time loads
- RETURN_ERRORS → shows only error rows
- RETURN_10_ROWS → shows first 10 valid rows (data preview)
- Validation does not advance the load history — re-running actual COPY will load the file

