## Schemas

### What is it?
- Namespace inside a database — groups related objects together
- Full object path: database.schema.object

```
CREATE SCHEMA sales_db.raw;
CREATE SCHEMA sales_db.staging;
CREATE SCHEMA sales_db.analytics;

USE SCHEMA sales_db.analytics;

-- Managed Access Schema (only schema owner can grant privileges)
CREATE SCHEMA sales_db.secure_schema WITH MANAGED ACCESS;
```

### Key Things to Remember
- Two auto-created schemas in every database:
- PUBLIC — default schema
- INFORMATION_SCHEMA — metadata views for that database
- Managed Access Schema = centralized privilege control — prevents object owners from granting access
