## 3. Function Naming Conventions

### Test Functions
```
# ✅ Pattern:  test_<what>_<condition>_<expected_result>

def test_filter_by_country_usa_returns_two_rows():       pass
def test_add_tier_column_revenue_above_5000_returns_gold(): pass
def test_fill_null_email_with_default_value():           pass
def test_join_customer_sales_left_join_preserves_all():  pass
def test_aggregate_revenue_empty_df_returns_empty():     pass

# ✅ Also acceptable shorter names
def test_filter_usa_customers():      pass
def test_gold_tier_assignment():      pass
def test_null_email_filled():         pass

# ❌ BAD — vague, unclear
def test_1():                         pass
def test_data():                      pass
def testCustomer():                   pass   # camelCase not allowed
def Test_filter():                    pass   # capital T not standard
```
### Fixture Functions

```
# ✅ Pattern:  <resource>_<description>   (NO "test_" prefix)

@pytest.fixture
def spark_session():                  pass   # SparkSession fixture
def sample_customer_df():             pass   # sample data fixture
def empty_dataframe():                pass   # edge case fixture
def customer_with_nulls_df():         pass   # specific condition
def expected_gold_tier_df():          pass   # expected output
def mock_s3_reader():                 pass   # mock fixture

# ❌ BAD
def test_spark():                     pass   # "test_" prefix = pytest runs it as test!
def SparkSession():                   pass   # PascalCase not for fixtures
def fixture_customer():               pass   # "fixture_" prefix redundant
```

### Helper / Utility Functions
```
# ✅ Pattern:  <verb>_<noun>  or  <action>_<description>

def create_dataframe(spark, data, schema):     pass
def generate_test_data(num_rows):              pass
def read_csv_as_df(spark, path):               pass
def build_expected_schema():                   pass
def get_row_by_id(df, id):                     pass

# ❌ BAD
def df1():                    pass   # meaningless
def getData():                pass   # camelCase
def CreateDF():               pass   # PascalCase
``` 

###  4. Class Naming Conventions
```
# ✅ Pattern:  Test<FeatureName>  or  Test<TransformationName>
# Uses PascalCase (each word capitalized)

class TestCustomerFilter:           pass
class TestSalesAggregation:         pass
class TestNullHandling:             pass
class TestSchemaValidation:         pass
class TestEdgeCases:                pass
class TestJoinTransformations:      pass
class TestCustomerTierAssignment:   pass

# ❌ BAD
class test_customer():              pass   # lowercase = not picked up reliably
class customerTest():               pass   # no "Test" prefix
class TESTCUSTOMER():               pass   # all caps
```

```
# Full class example with proper naming
class TestAddCustomerTier:

    def test_gold_tier_high_revenue(self, spark):         pass
    def test_silver_tier_medium_revenue(self, spark):     pass
    def test_bronze_tier_low_revenue(self, spark):        pass
    def test_tier_column_added_to_schema(self, spark):    pass
    def test_tier_null_revenue_defaults_to_bronze(self):  pass
```


### Variable Naming Conventions

```
def test_customer_tier(spark):

    # ─── Input data ───────────────────────────────────────
    input_data = [(1, "Alice", 6000.0)]        # ✅ "input_data"
    input_df   = spark.createDataFrame(...)    # ✅ "input_df"

    # ─── Result / Actual ──────────────────────────────────
    result_df   = add_customer_tier(input_df)  # ✅ "result_df"
    actual_df   = add_customer_tier(input_df)  # ✅ "actual_df"
    actual      = result_df.collect()[0]       # ✅ "actual"

    # ─── Expected ─────────────────────────────────────────
    expected_df   = spark.createDataFrame(...) # ✅ "expected_df"
    expected_tier = "Gold"                     # ✅ "expected_<field>"
    expected_count = 3                         # ✅ "expected_count"

    # ─── Intermediate ─────────────────────────────────────
    filtered_df   = result_df.filter(...)      # ✅ descriptive
    gold_rows     = result_df.filter(...)      # ✅ descriptive
    row_count     = result_df.count()          # ✅ "row_count"
    column_names  = result_df.columns          # ✅ "column_names"

    # ─── Schema ───────────────────────────────────────────
    expected_schema   = StructType([...])      # ✅ "expected_schema"
    actual_schema     = result_df.schema       # ✅ "actual_schema"

    # ❌ BAD
    df1   = spark.createDataFrame(...)         # meaningless
    d     = result_df.collect()                # too short
    temp  = add_customer_tier(input_df)        # vague
    x     = 3                                  # no context
```

### 7. conftest.py Naming Conventions
```
# ─── SparkSession Fixtures ────────────────────────────────────────
@pytest.fixture(scope="session")
def spark():                          pass   # ✅ standard name
def spark_session():                  pass   # ✅ also common

# ─── Input DataFrame Fixtures ─────────────────────────────────────
@pytest.fixture
def customer_df():                    pass   # ✅ <entity>_df
def sales_df():                       pass   # ✅
def sample_customer_df():             pass   # ✅ "sample_" prefix for test data
def raw_customer_df():                pass   # ✅ "raw_" prefix for unprocessed data
def customer_with_nulls_df():         pass   # ✅ describe the condition

# ─── Expected Output Fixtures ─────────────────────────────────────
@pytest.fixture
def expected_customer_df():           pass   # ✅ "expected_" prefix
def expected_aggregated_df():         pass   # ✅

# ─── Config / Setting Fixtures ────────────────────────────────────
@pytest.fixture
def spark_config():                   pass   # ✅
def test_config():                    pass   # ✅
def db_connection():                  pass   # ✅
def s3_client():                      pass   # ✅
```

### 8. Key Terminologies

```
TERM                  MEANING
────────────────────  ────────────────────────────────────────────────────────
Test Discovery        pytest automatically finds test files/functions
                      based on naming patterns (test_*.py, *_test.py)

Fixture               Reusable setup/teardown function decorated with
                      @pytest.fixture — provides data or resources to tests

conftest.py           Special file pytest auto-loads — holds shared fixtures
                      accessible by all tests in same/sub directories

Scope                 How long a fixture lives:
                       session  → entire test run (once)
                       module   → per file
                       class    → per class
                       function → per test (default)

Parametrize           Run same test with multiple input sets using
                      @pytest.mark.parametrize

Marker                Label/tag applied to tests using @pytest.mark.<name>
                      Used to group/filter test execution

Assert                Python statement to verify expected vs actual values
                      pytest rewrites assert for detailed failure messages

Yield Fixture         Fixture using "yield" to separate setup from teardown

Mock / Patch          Replace real objects/functions with fake ones
                      during testing to isolate units

Monkeypatch           pytest built-in fixture to modify objects,
                      env variables, or functions temporarily

Side Effect           What a mock does when called (raise error, return value)

Spy                   A mock that also calls the real function
                      (records calls but doesn't replace behavior)

Stub                  Returns hardcoded/predefined values
                      (simpler than a full mock)

AAA Pattern           Arrange → Act → Assert (standard test structure)

Test Suite            Collection of test files/classes/functions

Test Run              Single execution of pytest command

Assertion Error       Raised when assert statement fails

Exception Testing     Using pytest.raises() to verify errors are thrown

Coverage              % of source code executed during tests
                      measured by pytest-cov

Chispa                PySpark-specific library for comparing DataFrames
                      in tests (assert_df_equality)

SUT                   System Under Test — the code being tested

DRY                   Don't Repeat Yourself — avoid duplicate test code

FIRST Principles      Fast, Isolated, Repeatable, Self-validating, Timely
```

### 9. AAA Pattern (Most Important Test Structure)
```
def test_add_customer_tier_gold(spark):

    # ─── ARRANGE ─────────────────────────────────────────
    # Set up input data and expected output
    input_data = [(1, "Alice", 6000.0)]
    input_df   = spark.createDataFrame(input_data, ["id", "name", "revenue"])
    expected_tier = "Gold"

    # ─── ACT ─────────────────────────────────────────────
    # Call the function being tested
    result_df = add_customer_tier(input_df)

    # ─── ASSERT ──────────────────────────────────────────
    # Verify the result matches expectation
    actual_tier = result_df.collect()[0]["tier"]
    assert actual_tier == expected_tier
```

---

### 10. Fixture Scope Visual


```
TEST SESSION (scope="session")
│
│   @pytest.fixture(scope="session")
│   def spark():  ← Created ONCE, shared by all tests
│   │
│   ├── TEST MODULE: test_customer.py  (scope="module")
│   │   │
│   │   │   @pytest.fixture(scope="module")
│   │   │   def module_data():  ← Created once per file
│   │   │   │
│   │   │   ├── TestFilterByCountry (scope="class")
│   │   │   │   │
│   │   │   │   │   @pytest.fixture(scope="class")
│   │   │   │   │   def class_setup():  ← Once per class
│   │   │   │   │   │
│   │   │   │   │   ├── test_filter_usa()     ← function scope fixture created/destroyed
│   │   │   │   │   ├── test_filter_uk()      ← function scope fixture created/destroyed
│   │   │   │   │   └── test_filter_empty()   ← function scope fixture created/destroyed
│   │   │   │
│   │   │   └── TestAddTier
│   │   │       ├── test_gold_tier()
│   │   │       └── test_silver_tier()
│   │
│   └── TEST MODULE: test_sales.py
│       ├── test_sales_aggregation()
│       └── test_sales_filter()
```

---
### 12. Common Anti-Patterns to Avoid
```
# ❌ 1. Testing too many things in one test
def test_everything():
    result = transform(df)
    assert result.count() == 5
    assert "tier" in result.columns
    assert result.filter(...).count() == 2
    assert result.schema == expected_schema
    # Too many assertions — hard to debug failures

# ✅ One test, one concern
def test_row_count_after_transform():     assert result.count() == 5
def test_tier_column_exists():            assert "tier" in result.columns


# ❌ 2. Hardcoded magic numbers
def test_revenue_sum():
    assert result == 13000.0     # where does 13000 come from?

# ✅ Named constants or comments
ALICE_REVENUE  = 5000.0
CAROL_REVENUE  = 8000.0
EXPECTED_TOTAL = ALICE_REVENUE + CAROL_REVENUE   # 13000.0
def test_usa_total_revenue():
    assert result == EXPECTED_TOTAL


# ❌ 3. Creating SparkSession inside tests
def test_something():
    spark = SparkSession.builder.getOrCreate()   # SLOW! Creates new session
    ...

# ✅ Use session-scoped fixture from conftest.py
def test_something(spark):   # injected via fixture
    ...


# ❌ 4. Using production-size data
def test_transform():
    df = spark.read.parquet("s3://prod-bucket/huge-file/")  # millions of rows

# ✅ Use small representative test data
def test_transform(sample_customer_df):    # 4-10 rows max
    ...


# ❌ 5. Not testing edge cases
def test_add_tier():
    # Only tests happy path
    assert tier_for_6000 == "Gold"

# ✅ Also test boundaries and edge cases
def test_add_tier_boundary_exactly_5000():  assert tier == "Gold"
def test_add_tier_null_revenue():           assert tier == "Bronze"
def test_add_tier_empty_dataframe():        assert count == 0
```

---
### Summary Cheatsheet


```
FILE          → test_<feature_name>.py
FOLDER        → tests/, unit/, integration/, e2e/
TEST FUNC     → test_<what>_<condition>_<expected>()
FIXTURE       → <resource>_<description>()
CLASS         → Test<FeatureName>
VARIABLE      → input_df, result_df, expected_df, actual
MARKER        → @pytest.mark.unit / slow / integration
STRUCTURE     → AAA: Arrange → Act → Assert
SHARED CODE   → conftest.py
CONFIG        → pytest.ini / pyproject.toml
COMPARISON    → chispa (assert_df_equality)
ONE TEST      → Tests ONE thing only
SCOPE ORDER   → session > module > class > function
```




