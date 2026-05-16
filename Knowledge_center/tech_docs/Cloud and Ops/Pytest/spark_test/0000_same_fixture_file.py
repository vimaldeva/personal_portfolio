# test_transform.py

import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


# ─── BASE FIXTURES ────────────────────────────────────────────────
@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder.master("local").appName("test").getOrCreate()
    yield spark
    spark.stop()


@pytest.fixture
def raw_customer_df(spark):
    """Base raw data."""
    data = [(1, "Alice", "usa", 5000.0), (2, " Bob ", "uk", 3000.0)]
    return spark.createDataFrame(data, ["id", "name", "country", "revenue"])


# ─── FIXTURE USING ANOTHER FIXTURE ───────────────────────────────
@pytest.fixture
def cleaned_customer_df(raw_customer_df):
    """Builds on raw_customer_df fixture."""
    return raw_customer_df \
        .withColumn("name",    F.trim(F.col("name"))) \
        .withColumn("country", F.upper(F.col("country")))


@pytest.fixture
def tiered_customer_df(cleaned_customer_df):
    """Builds on cleaned_customer_df fixture."""
    return cleaned_customer_df.withColumn(
        "tier",
        F.when(F.col("revenue") >= 5000, "Gold").otherwise("Silver")
    )


# ─── TESTS ────────────────────────────────────────────────────────
def test_raw_has_lowercase_country(raw_customer_df):
    countries = [r["country"] for r in raw_customer_df.select("country").collect()]
    assert "usa" in countries                   # raw — lowercase

def test_cleaned_country_is_uppercase(cleaned_customer_df):
    countries = [r["country"] for r in cleaned_customer_df.select("country").collect()]
    assert "USA" in countries                   # cleaned — uppercase

def test_tiered_has_tier_column(tiered_customer_df):
    assert "tier" in tiered_customer_df.columns # tiered — has tier