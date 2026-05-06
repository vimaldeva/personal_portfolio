## Stored Procedures (PL/pgSQL)

### What is it?
- Pre-written SQL logic stored in Redshift that can be executed by name
- Supports loops, conditionals, variables, transactions
- Written in PL/pgSQL (similar to PostgreSQL)


```
CREATE OR REPLACE PROCEDURE load_and_clean_orders(load_date DATE)
AS $$
BEGIN
    -- Step 1: Load staging
    EXECUTE 'COPY orders_staging FROM ''s3://bucket/orders/'' IAM_ROLE ''...''';

    -- Step 2: Delete existing records for the date
    DELETE FROM orders WHERE order_date = load_date;

    -- Step 3: Insert from staging
    INSERT INTO orders SELECT * FROM orders_staging;

    -- Step 4: Cleanup
    DROP TABLE orders_staging;

    RAISE INFO 'Load complete for %', load_date;
END;
$$ LANGUAGE plpgsql;

-- Execute it
CALL load_and_clean_orders('2024-01-15');
```

### Key Things to Remember
- Stored procedures run inside Redshift — no external compute needed
- Supports transactions — COMMIT/ROLLBACK inside procedures
- Can call other stored procedures (nested calls)
- Good for encapsulating ETL logic that runs entirely in Redshift
- Cannot return result sets directly — use temp tables to pass results out
- Check existing procedures:


```
SELECT * FROM information_schema.routines
WHERE routine_type = 'PROCEDURE';
```
---

