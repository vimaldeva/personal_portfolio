## Federated Queries (RDS, Aurora)

## What is it?
- Query data live from RDS or Aurora directly from Redshift
- No need to extract/load operational DB data into Redshift first
- Query and join across Redshift + RDS/Aurora in one SQL statement

Analogy:

Redshift calls RDS on the phone and asks for data in real-time
Instead of making RDS send a letter first (ETL/load)

```
Redshift query references external RDS/Aurora table
        ↓
Redshift connects to RDS/Aurora via VPC
        ↓
Fetches data live from operational DB
        ↓
Joins with Redshift data and returns result
```

```
-- Create external schema pointing to RDS/Aurora
CREATE EXTERNAL SCHEMA rds_schema
FROM POSTGRES
DATABASE 'app_db'
URI 'rds-endpoint.rds.amazonaws.com'
IAM_ROLE 'arn:aws:iam::123:role/RedshiftRole'
SECRET_ARN 'arn:aws:secretsmanager:...';

-- Join Redshift table with RDS table
SELECT r.customer_id, r.name, s.total_orders
FROM rds_schema.customers r
JOIN redshift_schema.orders s ON r.customer_id = s.customer_id;
```

## Key Things to Remember
- Requires VPC connectivity between Redshift and RDS — same VPC or VPC peering
- Uses Secrets Manager to store RDS credentials
- Supports PostgreSQL and MySQL (RDS/Aurora)
- Don't use for heavy aggregations on RDS — pushes load onto operational DB
- Best for enriching Redshift data with small fresh lookups from RDS