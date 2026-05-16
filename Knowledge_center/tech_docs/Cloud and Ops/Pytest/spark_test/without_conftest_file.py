# test_customer.py  ← fixtures AND tests in SAME file

import pytest
from pyspark.sql import SparkSession
from src.transformations.customer_transform import add_customer_tier


# ─── FIXTURES DEFINED IN SAME FILE ───────────────────────────────
@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("test")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    yield spark
    spark.stop()


@pytest.fixture
def customer_df(spark):
    data = [
        (1, "Alice", "USA", 5000.0),
        (2, "Bob",   "UK",  3000.0),
        (3, "Carol", "USA", 8000.0),
    ]
    return spark.createDataFrame(data, ["id", "name", "country", "revenue"])


@pytest.fixture
def empty_df(spark):
    return spark.createDataFrame([], "id INT, name STRING, revenue DOUBLE")


# ─── TESTS USING THOSE FIXTURES ───────────────────────────────────
def test_row_count(customer_df):
    assert customer_df.count() == 3

def test_tier_column_added(customer_df):
    result = add_customer_tier(customer_df)
    assert "tier" in result.columns

def test_empty_dataframe(empty_df):
    result = add_customer_tier(empty_df)
    assert result.count() == 0