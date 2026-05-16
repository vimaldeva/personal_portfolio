## PUT Command
### What is it?
Uploads files from your local machine to an internal stage
Only works from Snowflake clients (SnowSQL, connectors) — NOT from Snowsight UI

```
-- Upload single file
PUT file:///home/user/orders.csv @my_stage;

-- Upload with auto-compression
PUT file:///home/user/orders.csv @my_stage
    AUTO_COMPRESS = TRUE;          -- compresses to GZIP automatically

-- Upload all CSVs from a folder
PUT file:///home/user/data/*.csv @my_stage;

-- Upload without overwriting existing files
PUT file:///home/user/orders.csv @my_stage
    OVERWRITE = FALSE;

-- Specify parallel threads for large files
PUT file:///home/user/large_file.csv @my_stage
    PARALLEL = 4;
```


### Key Things to Remember
PUT automatically compresses files (GZIP) unless disabled
Files uploaded in parallel — faster for large files
PUT only works with internal stages (User, Table, Named internal)
Cannot use PUT from Snowsight web UI — use SnowSQL CLI or SDK