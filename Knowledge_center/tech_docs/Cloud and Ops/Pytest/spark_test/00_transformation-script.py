# src/transformations/customer_transform.py
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType


def filter_by_country(df: DataFrame, country: str) -> DataFrame:
    """Filter customers by country."""
    return df.filter(F.col("country") == country)


def fill_missing_emails(df: DataFrame, default: str = "unknown@example.com") -> DataFrame:
    """Fill null emails with a default value."""
    return df.fillna({"email": default})


def add_customer_tier(df: DataFrame) -> DataFrame:
    """
    Classify customers into tiers based on revenue:
      - Gold  : revenue >= 5000
      - Silver: revenue >= 2000
      - Bronze: revenue < 2000
    """
    return df.withColumn(
        "tier",
        F.when(F.col("revenue") >= 5000, "Gold")
         .when(F.col("revenue") >= 2000, "Silver")
         .otherwise("Bronze")
    )


def normalize_country_code(df: DataFrame) -> DataFrame:
    """Uppercase and trim country codes."""
    return df.withColumn("country", F.upper(F.trim(F.col("country"))))


def aggregate_revenue_by_country(df: DataFrame) -> DataFrame:
    """Total revenue grouped by country."""
    return (
        df.groupBy("country")
          .agg(
              F.sum("revenue").alias("total_revenue"),
              F.count("customer_id").alias("customer_count"),
              F.avg("revenue").alias("avg_revenue")
          )
          .orderBy("country")
    )


def join_customer_sales(customer_df: DataFrame, sales_df: DataFrame) -> DataFrame:
    """Join customer and sales data."""
    return (
        customer_df.join(sales_df, on="customer_id", how="left")
                   .select(
                       "customer_id", "name", "country",
                       "order_id", "order_date", "amount", "category"
                   )
    )