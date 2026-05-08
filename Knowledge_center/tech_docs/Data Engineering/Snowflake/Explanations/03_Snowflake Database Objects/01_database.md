## Databases

### What is it?
- Top-level container for all Snowflake objects
- Each database contains schemas → schemas contain tables, views, etc.

```
CREATE DATABASE sales_db;
USE DATABASE sales_db;
DROP DATABASE sales_db;

-- Clone entire database (zero-copy)
CREATE DATABASE sales_db_dev CLONE sales_db;
```

### Key Things to Remember
- Every Snowflake account has a built-in SNOWFLAKE database (read-only, usage metadata)
- Databases can be replicated across regions/clouds (Enterprise+)
- INFORMATION_SCHEMA exists in every database — contains metadata about that DB