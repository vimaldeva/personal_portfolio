## Stored Procedures

### What is it?
- Reusable procedural logic that runs inside Snowflake
- Supports loops, conditionals, error handling, transactions
- Written in: JavaScript, Python, Scala, Java, Snowpark, SQL

```
-- SQL stored procedure
CREATE OR REPLACE PROCEDURE upsert_orders(load_date DATE)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    -- Step 1: Delete existing
    DELETE FROM orders WHERE order_date = :load_date;

    -- Step 2: Insert from staging
    INSERT INTO orders
    SELECT * FROM orders_staging WHERE order_date = :load_date;

    -- Step 3: Cleanup
    DELETE FROM orders_staging WHERE order_date = :load_date;

    RETURN 'Success: ' || :load_date;
END;
$$;

-- Call the procedure
CALL upsert_orders('2024-01-15');
```

```
-- Python stored procedure (Snowpark)
CREATE OR REPLACE PROCEDURE process_orders()
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'run'
AS
$$
def run(session):
    df = session.table("orders_staging")
    df.write.mode("append").save_as_table("orders_final")
    return f"Loaded {df.count()} rows"
$$;
```

### Key Things to Remember
- Procedures run with caller's rights or owner's rights — set via EXECUTE AS CALLER/OWNER
- Procedures can call other procedures — nesting supported
- Unlike functions — procedures can execute DML (INSERT, UPDATE, DELETE)
- Use procedures to encapsulate multi-step ETL logic