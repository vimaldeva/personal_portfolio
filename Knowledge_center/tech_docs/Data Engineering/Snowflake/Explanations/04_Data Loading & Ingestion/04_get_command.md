## GET Command
### What is it?
Downloads files from an internal stage to your local machine
Reverse of PUT

```
-- Download specific file
GET @my_stage/orders.csv file:///home/user/downloads/;

-- Download all files matching pattern
GET @my_stage/orders_2024 file:///home/user/downloads/;

-- Download with parallel threads
GET @my_stage/large_file.csv.gz file:///home/user/downloads/
    PARALLEL = 4;
```

### Key Things to Remember
- GET only works with internal stages — not external (S3/Azure/GCS)
- For external stages → use AWS CLI / Azure Storage tools to download
- Downloaded files may be GZIP compressed — decompress after download
