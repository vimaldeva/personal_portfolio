class TestJoinCustomerSales:

    def test_join_row_count(self, sample_customer_df, sample_sales_df):
        result = join_customer_sales(sample_customer_df, sample_sales_df)
        # customer 1 has 2 orders, customer 2 has 2, customer 3 has 1, customer 4 has 0 (left join)
        assert result.count() == 6  # 2+2+1+1(null row for Dave)

    def test_left_join_preserves_all_customers(self, sample_customer_df, sample_sales_df):
        result = join_customer_sales(sample_customer_df, sample_sales_df)
        customer_ids = [row["customer_id"] for row in result.select("customer_id").distinct().collect()]
        assert 4 in customer_ids  # Dave with no orders is still present

    def test_join_no_extra_columns(self, sample_customer_df, sample_sales_df):
        result = join_customer_sales(sample_customer_df, sample_sales_df)
        expected_cols = {"customer_id", "name", "country", "order_id", "order_date", "amount", "category"}
        assert set(result.columns) == expected_cols