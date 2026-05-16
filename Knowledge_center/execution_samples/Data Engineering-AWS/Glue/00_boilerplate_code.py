import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext, SparkConf
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql import Window
from delta.tables import DeltaTable # Required for Merge


conf = SparkConf()

conf.set("spark.sql.adaptive.enabled", "true")
conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
conf.set("spark.sql.shuffle.partitions", "200")
conf.set("spark.sql.iceberg.handle-timestamp-without-timezone", "true")

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext(conf=conf)
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

CATALOG         = "glue_catalog"
WAREHOUSE_PATH  = "s3://aaaaaaaaa/gold-curated/"
SOURCE_DB       = "silver_db"
SOURCE_TABLE    = "customer_table"
TARGET_DB       = "gold_db"
TARGET_TABLE    = "target_customer"
TOP_N_PER_DATE  = 0   # 0 = keep all; set to e.g. 100 for top 100 per date

FULL_SOURCE     = f"{CATALOG}.{SOURCE_DB}.{SOURCE_TABLE}"
FULL_TARGET     = f"{CATALOG}.{TARGET_DB}.{TARGET_TABLE}"

print("===== CONFIG =====")
print(f"Source table  : {FULL_SOURCE}")
print(f"Target table  : {FULL_TARGET}")

source_df = (
    spark.read.table(FULL_SOURCE)
    .filter(F.col("device_active_ind") == True))

## ................


df.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .option("path", s3_path) \
    .saveAsTable(f"{database_name}.{table_name}")

##  OR using upsert format below
##
##
##

full_table_name = f"{database_name}.{table_name}"

# 1. Create Sample Upsert Data
# Assume 'id' is our primary key. 
# We are updating Alice's name and adding a new record for Charlie.
data = [
    (1, "Alice Updated", "2023-10-05"), 
    (3, "Charlie", "2023-10-05")
]
columns = ["id", "name", "date"]
updates_df = spark.createDataFrame(data, columns)

# 2. Check if the table exists in the Glue Catalog
table_exists = spark.catalog._jcatalog.tableExists(database_name, table_name)

if not table_exists:
    # Initial Load: If table doesn't exist, create it
    print(f"Table {full_table_name} does not exist. Performing initial write.")
    updates_df.write \
        .format("delta") \
        .mode("overwrite") \
        .option("path", s3_path) \
        .saveAsTable(full_table_name)
else:
    # UPSERT (MERGE) Logic
    print(f"Table {full_table_name} exists. Performing Upsert (Merge).")
    
    # Access the existing Delta table using the path
    dt = DeltaTable.forPath(spark, s3_path)
    
    # Execute Merge operation
    dt.alias("target").merge(
        updates_df.alias("source"),
        "target.id = source.id"  # The join condition
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()

job.commit()


## Make sure in the Glue job paramaeters you are giving the table format as Delta

