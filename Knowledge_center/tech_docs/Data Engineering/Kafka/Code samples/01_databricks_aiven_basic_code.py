# This combines your cert and key into one file that Spark can read easily
cert_path = "/Volumes/main/default/kafka_files/service.cert"
key_path = "/Volumes/main/default/kafka_files/service.key"
combined_path = "/Volumes/main/default/kafka_files/combined.pem"

with open(cert_path, 'r') as f:
    cert_data = f.read()
with open(key_path, 'r') as f:
    key_data = f.read()

with open(combined_path, 'w') as f:
    f.write(cert_data)
    f.write("\n")
    f.write(key_data)

print(f"Combined file created at: {combined_path}")

# --- CONFIGURATION ---
# Use the standard SSL port (usually 26267) from Aiven Overview
kafka_uri = "kafka-vimal-vimaldeva10-ebe6.k.aivencloud.com:26267" 
topic_name = "test-topic"

# Paths in your Volume
ca_path = "/Volumes/main/default/kafka_files/ca.pem"
combined_cert_path = "/Volumes/main/default/kafka_files/combined.pem"
checkpoint_path = "/Volumes/main/default/kafka_files/checkpoint_mtls_v1"

# --- THE CODE ---
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_uri) \
    .option("subscribe", topic_name) \
    .option("kafka.security.protocol", "SSL") \
    .option("kafka.ssl.truststore.type", "PEM") \
    .option("kafka.ssl.truststore.location", ca_path) \
    .option("kafka.ssl.keystore.type", "PEM") \
    .option("kafka.ssl.keystore.location", combined_cert_path) \
    .option("kafka.ssl.enabled.protocols", "TLSv1.2") \
    .option("kafka.ssl.endpoint.identification.algorithm", "") \
    .option("startingOffsets", "earliest") \
    .load()

# --- THE DISPLAY ---
display(df.selectExpr("CAST(value AS STRING)"), checkpointLocation=checkpoint_path)

from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# 1. Define what your data looks like (Schema)
schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("action", StringType(), True),
    StructField("item", StringType(), True)
])

# 2. Take your existing 'df' and parse the JSON
# (Assuming 'df' is the variable from your successful connection code)
readable_df = df.selectExpr("CAST(value AS STRING) as json_string") \
    .select(from_json(col("json_string"), schema).alias("data")) \
    .select("data.*")

# 3. Display it
display(readable_df, checkpointLocation="/Volumes/main/default/kafka_files/checkpoint_display")

# 1. Prepare the data (Convert binary to string)
streaming_df = df.selectExpr("CAST(value AS STRING) as message_content", "current_timestamp() as arrival_time")

# 2. Write the stream to a Delta Table
# This will create a table named 'vimal_kafka_table'
query = streaming_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .trigger(availableNow= True)\
    .option("checkpointLocation", "/Volumes/main/default/kafka_files/checkpoint_table") \
    .toTable("main.default.vimal_kafka_table")