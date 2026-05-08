## File Formats
- A named object that defines how to parse files during load/unload
- Reuse across multiple COPY commands

```
-- Create named file format
CREATE FILE FORMAT my_csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE;

CREATE FILE FORMAT my_json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE;

CREATE FILE FORMAT my_parquet_format
    TYPE = 'PARQUET'
    SNAPPY_COMPRESSION = TRUE;

-- Use in COPY
COPY INTO orders FROM @my_stage
FILE_FORMAT = my_csv_format;
```

### Supported Formats
CSV, JSON, AVRO, ORC, PARQUET, XML