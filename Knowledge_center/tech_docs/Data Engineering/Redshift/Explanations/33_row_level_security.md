## Row-Level Security (RLS)

### What is it?
- Restricts which rows a user can see in a table based on a policy
- Same table, same query — different users see different rows

Analogy:
- All sales reps query the orders table
- Rep from EAST region sees only EAST orders
- Rep from WEST region sees only WEST orders
- Same table, same SQL — filtered automatically

### How it Works
```
-- Step 1: Create RLS Policy
CREATE RLS POLICY region_policy
WITH (region VARCHAR)
USING (region = current_user);   -- user only sees rows matching their username

-- Step 2: Attach policy to table
ATTACH RLS POLICY region_policy ON orders TO ROLE sales_role;

-- Step 3: Enable RLS on table
ALTER TABLE orders ROW LEVEL SECURITY ON;
```

```
User: east_rep queries → SELECT * FROM orders
Redshift automatically adds → WHERE region = 'east_rep'
User sees only their rows — unaware of filter ✅
```

### Key Things to Remember
- Superusers and users with IGNORE RLS privilege bypass all RLS policies
- Multiple policies on same table → rows must match ALL policies (AND logic)
- RLS adds no visible filter in the query — completely transparent to user
- Check existing policies:

```
SELECT * FROM svv_rls_policy;
```