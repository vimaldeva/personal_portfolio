## Functions (UDFs & UDTFs)
- UDF (User Defined Function — Scalar)
- Takes input → returns one value per row

```
-- SQL UDF
CREATE FUNCTION calculate_tax(amount FLOAT, rate FLOAT)
RETURNS FLOAT
AS 'amount * rate';

SELECT order_id, calculate_tax(revenue, 0.08) as tax FROM orders;

-- Python UDF
CREATE FUNCTION mask_email(email STRING)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
HANDLER = 'mask'
AS
$$
def mask(email):
    parts = email.split('@')
    return parts[0][0] + '***@' + parts[1]
$$;
```
### UDTF (User Defined Table Function)
- Takes input → returns multiple rows (a table)
```
-- Python UDTF — splits a string into multiple rows
CREATE FUNCTION split_tags(tags STRING)
RETURNS TABLE (tag STRING)
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
HANDLER = 'TagSplitter'
AS
$$
class TagSplitter:
    def process(self, tags):
        for tag in tags.split(','):
            yield (tag.strip(),)
$$;

-- Use UDTF in query
SELECT order_id, t.tag
FROM orders, TABLE(split_tags(orders.tags)) t;
```

### UDF vs UDTF vs Stored Procedure
|  | UDF | UDTF | Stored Procedure |
| :-- | :-- | :-- | :-- |
| Returns | Single value | Multiple rows | Variant / String |
| Used in SELECT | ✅ | ✅ | ❌ |
| Executes DML | ❌ | ❌ | ✅ |
| Languages | SQL, Python, Java, JS, Scala | Python, Java, Scala | All + Snowpark |


