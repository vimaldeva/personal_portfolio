# tests/test_schema.py
from pyspark.sql.types import (
    StructType, StructField, StringType,
    IntegerType, DoubleType
)

class TestSchemaValidation:

    EXPECTED_SCHEMA = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("name",        StringType(),  True),
        StructField("email",       StringType(),  True),
        StructField("country",     StringType(),  True),
        StructField("revenue",     DoubleType(),  True),
    ])

    def test_input_schema_matches(self, sample_customer_df):
        assert sample_customer_df.schema == self.EXPECTED_SCHEMA

    def test_tier_column_is_string(self, sample_customer_df):
        result = add_customer_tier(sample_customer_df)
        tier_type = dict(result.dtypes)["tier"]
        assert tier_type == "string"

    def test_output_has_no_extra_columns(self, sample_customer_df):
        result = add_customer_tier(sample_customer_df)
        assert len(result.columns) == len(sample_customer_df.columns) + 1