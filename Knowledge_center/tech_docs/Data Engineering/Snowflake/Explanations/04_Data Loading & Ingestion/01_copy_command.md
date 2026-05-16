## COPY INTO Command

### What is it?
- Primary bulk loading command in Snowflake — loads files from a stage into a table
- Runs on a virtual warehouse — parallel across all nodes
- Tracks loaded files — won't reload same file twice (unless FORCE=TRUE)

```
-- Basic COPY from external stage
COPY INTO orders
FROM @my_s3_stage
FILE_FORMAT = (TYPE = 'PARQUET');

-- With options
COPY INTO orders
FROM @my_s3_stage/2024/01/
FILE_FORMAT = (FORMAT_NAME = 'my_csv_format')
ON_ERROR = 'CONTINUE'
PURGE = TRUE;

-- Load specific files
COPY INTO orders
FROM @my_s3_stage
FILES = ('orders_jan.csv', 'orders_feb.csv');

-- Load with pattern match
COPY INTO orders
FROM @my_s3_stage
PATTERN = '.*orders_2024.*\.parquet';
```

