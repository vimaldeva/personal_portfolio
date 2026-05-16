## File Formats

CSV 
```
CREATE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE
    ENCODING = 'UTF-8';
```

JSON
```
CREATE FILE FORMAT json_format
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE      -- remove outer [] from JSON array
    STRIP_NULL_VALUES = FALSE
    IGNORE_UTF8_ERRORS = FALSE;
```

```
CREATE FILE FORMAT parquet_format
    TYPE = 'PARQUET'
    SNAPPY_COMPRESSION = TRUE;    -- or NONE, AUTO
```

### Format Comparison
| Format | Best For | Compression | Schema |
| :-- | :-- | :-- | :-- |
| CSV | Simple, universal | External (GZIP) | None |
| JSON | Semi-structured data | Built-in | None |
| Parquet | Columnar, analytics | Built-in (Snappy) | Embedded |
| Avro | Streaming, row-based | Built-in | Embedded |
| ORC | Hive ecosystem | Built-in | Embedded |

Best for Snowflake loading: Parquet — columnar, compressed, schema embedded



