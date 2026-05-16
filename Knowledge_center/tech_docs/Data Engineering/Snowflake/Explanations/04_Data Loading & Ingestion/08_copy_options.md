## COPY Options (ON_ERROR, PURGE, FORCE)

### ON_ERROR — Error Handling

```
-- ABORT_STATEMENT (default) — stop entire load on first error
COPY INTO orders FROM @stage ON_ERROR = 'ABORT_STATEMENT';

-- CONTINUE — skip bad rows, load everything else
COPY INTO orders FROM @stage ON_ERROR = 'CONTINUE';

-- SKIP_FILE — skip entire file if it has any error
COPY INTO orders FROM @stage ON_ERROR = 'SKIP_FILE';

-- SKIP_FILE_n — skip file if it has more than n errors
COPY INTO orders FROM @stage ON_ERROR = 'SKIP_FILE_5';

-- SKIP_FILE_n% — skip file if more than n% of rows have errors
COPY INTO orders FROM @stage ON_ERROR = 'SKIP_FILE_10%';
```

### PURGE — Delete Files After Load
```
-- Delete files from stage after successful load
COPY INTO orders FROM @stage PURGE = TRUE;

-- Keep files after load (default)
COPY INTO orders FROM @stage PURGE = FALSE;
```

### FORCE — Reload Already-Loaded Files
```
-- By default Snowflake skips already-loaded files
-- FORCE = TRUE overrides this — reloads even if already loaded
COPY INTO orders FROM @stage FORCE = TRUE;
```

### Other Useful Options
```
COPY INTO orders FROM @stage
    FILES = ('file1.csv', 'file2.csv')  -- load specific files
    PATTERN = '.*2024.*\.csv'           -- load files matching regex
    TRUNCATECOLUMNS = TRUE              -- truncate values exceeding column length
    FORCE = FALSE                       -- don't reload already-loaded files
    PURGE = FALSE                       -- keep files after load
    ON_ERROR = 'CONTINUE';             -- skip bad rows
```


