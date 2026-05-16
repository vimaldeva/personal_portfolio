## 1. File Naming Conventions

```
✅ CORRECT                          ❌ INCORRECT
──────────────────────────────────  ──────────────────────────────────
test_customer.py                    customer.py
test_sales_transform.py             salesTransform.py
test_utils.py                       Test_Utils.py
test_order_processing.py            testOrderProcessing.py
conftest.py                         conf.py / config.py
```

```
📌 Rules:
  - Must start with  "test_"  OR end with  "_test"
  - All lowercase
  - Words separated by underscore (_)  ← snake_case
  - Descriptive of what is being tested
```

```
# Both are valid — "test_" prefix is most common
test_customer.py       ✅  (preferred)
customer_test.py       ✅  (also valid)
```
