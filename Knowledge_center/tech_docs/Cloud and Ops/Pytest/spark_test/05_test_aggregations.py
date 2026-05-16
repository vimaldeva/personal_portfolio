class TestAggregateRevenueByCountry:

    def test_correct_country_count(self, sample_customer_df):
        result = aggregate_revenue_by_country(sample_customer_df)
        # USA, UK, CA = 3 countries
        assert result.count() == 3

    def test_usa_total_revenue(self, sample_customer_df):
        result = aggregate_revenue_by_country(sample_customer_df)
        usa_row = result.filter(F.col("country") == "USA").collect()[0]
        assert usa_row["total_revenue"] == 13000.0   # 5000 + 8000

    def test_customer_count_per_country(self, sample_customer_df):
        result = aggregate_revenue_by_country(sample_customer_df)
        usa_row = result.filter(F.col("country") == "USA").collect()[0]
        assert usa_row["customer_count"] == 2

    def test_avg_revenue_calculation(self, sample_customer_df):
        result = aggregate_revenue_by_country(sample_customer_df)
        usa_row = result.filter(F.col("country") == "USA").collect()[0]
        assert usa_row["avg_revenue"] == 6500.0  # (5000 + 8000) / 2

    def test_output_columns(self, sample_customer_df):
        result = aggregate_revenue_by_country(sample_customer_df)
        expected_cols = {"country", "total_revenue", "customer_count", "avg_revenue"}
        assert set(result.columns) == expected_cols