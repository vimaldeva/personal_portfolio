class TestAddCustomerTier:

    def test_tier_column_added(self, sample_customer_df):
        result = add_customer_tier(sample_customer_df)
        assert "tier" in result.columns

    def test_gold_tier_assignment(self, sample_customer_df):
        result = add_customer_tier(sample_customer_df)
        gold = result.filter(F.col("tier") == "Gold")
        names = [row["name"] for row in gold.select("name").collect()]
        assert sorted(names) == ["Alice", "Carol"]

    def test_bronze_tier_assignment(self, sample_customer_df):
        result = add_customer_tier(sample_customer_df)
        bronze = result.filter(F.col("tier") == "Bronze")
        assert bronze.count() == 1
        assert bronze.collect()[0]["name"] == "Dave"

    def test_silver_tier_assignment(self, sample_customer_df):
        result = add_customer_tier(sample_customer_df)
        silver = result.filter(F.col("tier") == "Silver")
        assert silver.collect()[0]["name"] == "Bob"

    @pytest.mark.parametrize("revenue, expected_tier", [
        (6000.0, "Gold"),
        (5000.0, "Gold"),
        (4999.0, "Silver"),
        (2000.0, "Silver"),
        (1999.0, "Bronze"),
        (0.0,    "Bronze"),
    ])
    def test_tier_boundaries(self, spark, revenue, expected_tier):
        data = [(1, "Test", revenue)]
        df = spark.createDataFrame(data, ["id", "name", "revenue"])
        result = add_customer_tier(df)
        tier = result.collect()[0]["tier"]
        assert tier == expected_tier