## Dynamic Data Masking (DDM)

## What is it?
- Shows masked/obfuscated version of sensitive data to unauthorized users
- Unlike Column-Level Security (which blocks access completely) — DDM shows data but hides the real value
- Different users see different versions of same column

Analogy:
- Credit card number: 4111-1111-1111-1234
- Admin sees: 4111-1111-1111-1234 (full)
- Support agent sees: ****-****-****-1234 (masked)
- Same column, same table — different views

### How it Works

```
-- Step 1: Create masking policy
CREATE MASKING POLICY mask_credit_card
WITH (credit_card VARCHAR)
USING ('****-****-****-' || RIGHT(credit_card, 4));

-- Step 2: Attach policy to column
ATTACH MASKING POLICY mask_credit_card
ON customers(credit_card)
TO ROLE support_role;        -- support sees masked value

-- Full access role (no masking policy attached = sees real data)
```
```
Admin queries        → 4111-1111-1111-1234  (real)
Support agent queries → ****-****-****-1234  (masked)
Same table, same column ✅
```

### Masking Options

```
-- Full mask
USING (NULL)                                        -- show NULL

-- Partial mask
USING ('***-**-' || RIGHT(ssn, 4))                 -- show last 4 digits

-- Hash mask
USING (MD5(email))                                  -- hash the value

-- Custom function mask
USING (mask_email_udf(email))                       -- use custom UDF
```

### Key Things to Remember

- DDM requires attached policy per role/user — no policy = sees real data
- Multiple masking policies on same column → lowest priority role policy applies
- DDM does not encrypt data — just changes what's displayed in query results
- Works with RLS and Column Security together for full data protection
- Check existing masking policies:

```
SELECT * FROM svv_masking_policy;
``` 
