# tests/test_edge_cases.py

class TestEdgeCases:

    def test_empty_dataframe(self, spark):
        """Transformation should handle empty DataFrames gracefully."""
        schema = ["customer_id", "name", "email", "country", "revenue"]
        empty_df = spark.createDataFrame([], 
            "customer_id INT, name STRING, email STRING, country STRING, revenue DOUBLE"
        )
        result = add_customer_tier(empty_df)
        assert result.count() == 0
        assert "tier" in result.columns

    def test_all_null_revenue(self, spark):
        """Handle all null revenue values."""
        data = [(1, "Alice", None), (2, "Bob", None)]
        df = spark.createDataFrame(data, ["id", "name", "revenue"])
        result = df.withColumn(
            "tier",
            F.when(F.col("revenue") >= 5000, "Gold")
             .when(F.col("revenue") >= 2000, "Silver")
             .otherwise("Bronze")
        )
        tiers = [row["tier"] for row in result.collect()]
        assert all(t == "Bronze" for t in tiers)

    def test_single_row_dataframe(self, spark):
        data = [(1, "Solo", "solo@test.com", "US", 9999.0)]
        df = spark.createDataFrame(data, 
            ["customer_id", "name", "email", "country", "revenue"]
        )
        result = add_customer_tier(df)
        assert result.count() == 1
        assert result.collect()[0]["tier"] == "Gold"

    def test_duplicate_records(self, spark):
        """Ensure no unintended deduplication in transformations."""
        data = [
            (1, "Alice", "USA", 5000.0),
            (1, "Alice", "USA", 5000.0),   # duplicate
        ]
        df = spark.createDataFrame(data, ["id", "name", "country", "revenue"])
        result = add_customer_tier(df)
        assert result.count() == 2