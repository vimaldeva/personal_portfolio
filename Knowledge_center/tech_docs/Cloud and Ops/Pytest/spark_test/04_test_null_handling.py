class TestFillMissingEmails:

    def test_null_email_filled(self, sample_customer_df):
        result = fill_missing_emails(sample_customer_df)
        null_count = result.filter(F.col("email").isNull()).count()
        assert null_count == 0

    def test_existing_emails_unchanged(self, sample_customer_df):
        result = fill_missing_emails(sample_customer_df)
        alice = result.filter(F.col("name") == "Alice").collect()[0]
        assert alice["email"] == "alice@example.com"

    def test_custom_default_email(self, sample_customer_df):
        result = fill_missing_emails(sample_customer_df, default="noreply@company.com")
        dave = result.filter(F.col("name") == "Dave").collect()[0]
        assert dave["email"] == "noreply@company.com"

    def test_no_nulls_in_input(self, spark):
        data = [(1, "Alice", "alice@test.com")]
        df = spark.createDataFrame(data, ["id", "name", "email"])
        result = fill_missing_emails(df)
        assert result.count() == 1