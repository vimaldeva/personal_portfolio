from pyspark.sql import SparkSession

# Create a Spark Session
spark = SparkSession.builder \
    .appName("TestApp") \
    .getOrCreate()

# Create a simple DataFrame
data = [("Alice", 34), ("Bob", 45), ("Charlie", 29)]
df = spark.createDataFrame(data, ["Name", "Age"])

df.show()