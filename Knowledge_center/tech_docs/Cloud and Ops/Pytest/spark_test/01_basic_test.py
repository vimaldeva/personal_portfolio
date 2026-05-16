# tests/test_customer.py
import pytest
from pyspark.sql import functions as F
from src.transformations.customer_transform import (
    filter_by_country,
    fill_missing_emails,
    add_customer_tier,
    normalize_country_code,
    aggregate_revenue_by_country,
    join_customer_sales,
)


class TestFilterByCountry:

    def test_filter_usa_customers(self, sample_customer_df):
        result = filter_by_country(sample_customer_df, "USA")
        assert result.count() == 2

    def test_filter_returns_correct_names(self, sample_customer_df):
        result = filter_by_country(sample_customer_df, "USA")
        names = [row["name"] for row in result.collect()]
        assert sorted(names) == ["Alice", "Carol"]

    def test_filter_no_match(self, sample_customer_df):
        result = filter_by_country(sample_customer_df, "INDIA")
        assert result.count() == 0

    def test_filter_preserves_schema(self, sample_customer_df):
        result = filter_by_country(sample_customer_df, "USA")
        assert result.columns == sample_customer_df.columns