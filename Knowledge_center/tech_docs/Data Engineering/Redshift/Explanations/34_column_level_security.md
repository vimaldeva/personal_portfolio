## Column-Level Security
### What is it?
- Controls which columns a user can access in a table
- Done via standard GRANT/REVOKE on specific columns

Analogy:
- HR table has name, salary, SSN
- Managers can see name + salary but not SSN
- Finance can see all columns

### How it Works
```
-- Grant access to specific columns only
GRANT SELECT (customer_name, order_date, region)
ON orders TO analyst_role;

-- Revoke access to sensitive column
REVOKE SELECT (salary) ON employees FROM analyst_role;
```

```
analyst_role runs → SELECT * FROM orders
Redshift returns  → only customer_name, order_date, region
salary, SSN columns → permission denied ✅
```

### Key Things to Remember
- Column grants work at role or user level
- User trying to SELECT * only gets permitted columns — no error, just filtered
- Combine with RLS for both row and column filtering simultaneously
- Table owner and superusers always see all columns
