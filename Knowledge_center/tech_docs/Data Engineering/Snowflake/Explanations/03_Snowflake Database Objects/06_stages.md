## Stages (Internal vs External)

### What is it?
- A named location where data files are stored before loading or after unloading
- Bridge between your files and Snowflake tables

#### Internal Stages (Snowflake manages the storage)

#### User Stage (auto-created per user)

```
-- Upload to your personal user stage
PUT file:///local/orders.csv @~;

-- List files in user stage
LIST @~;

-- Load from user stage
COPY INTO orders FROM @~/orders.csv;
```
#### Table Stage (auto-created per table)

```
-- Each table has its own stage
PUT file:///local/orders.csv @%orders;
COPY INTO orders FROM @%orders;
```

#### Named Internal Stage (explicit, shared)
```
CREATE STAGE my_internal_stage
    FILE_FORMAT = (TYPE = 'CSV');

PUT file:///local/orders.csv @my_internal_stage;
COPY INTO orders FROM @my_internal_stage;
```

#### External Stages (points to S3/Azure/GCS)
```
-- S3 External Stage
CREATE STAGE my_s3_stage
    URL = 's3://my-bucket/data/'
    CREDENTIALS = (AWS_ROLE = 'arn:aws:iam::123:role/SnowflakeRole')
    FILE_FORMAT = (TYPE = 'PARQUET');

-- Load from external stage
COPY INTO orders FROM @my_s3_stage;

-- List files in external stage
LIST @my_s3_stage;
```

#### Internal vs External
| Factor | Internal Stage | External Stage |
| :-- | :-- | :-- |
| Storage | Snowflake manages | Your S3/Azure/GCS |
| Cost | Snowflake storage pricing | Your cloud storage cost |
| Access | Snowflake only | You + Snowflake |
| Use case | Temporary upload/download | Ongoing data pipeline from cloud |





