# tests/conftest.py
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """
    Create a SparkSession once for the entire test session.
    scope="session" avoids creating/stopping Spark multiple times.
    """
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("pytest-pyspark-tests")
        .config("spark.sql.shuffle.partitions", "2")   # faster for small test data
        .config("spark.default.parallelism", "2")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")   # suppress noisy logs
    yield spark
    spark.stop()


@pytest.fixture(scope="function")
def sample_customer_df(spark):
    """Reusable sample customer DataFrame."""
    data = [
        (1, "Alice", "alice@example.com", "USA", 5000.0),
        (2, "Bob",   "bob@example.com",   "UK",  3000.0),
        (3, "Carol", "carol@example.com", "USA", 8000.0),
        (4, "Dave",  None,                "CA",  1500.0),
    ]
    schema = ["customer_id", "name", "email", "country", "revenue"]
    return spark.createDataFrame(data, schema)


@pytest.fixture(scope="function")
def sample_sales_df(spark):
    """Reusable sample sales DataFrame."""
    data = [
        (101, 1, "2023-01-15", 500.0, "Electronics"),
        (102, 2, "2023-01-16", 300.0, "Clothing"),
        (103, 1, "2023-02-10", 700.0, "Electronics"),
        (104, 3, "2023-02-20", 200.0, "Books"),
        (105, 2, "2023-03-05", 150.0, None),
    ]
    schema = ["order_id", "customer_id", "order_date", "amount", "category"]
    return spark.createDataFrame(data, schema)