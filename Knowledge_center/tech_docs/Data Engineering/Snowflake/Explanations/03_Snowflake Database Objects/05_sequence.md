## Sequences

### What is it?
- Auto-incrementing number generator — generates unique sequential integers
- Used to create surrogate keys

```
CREATE SEQUENCE order_seq START = 1 INCREMENT = 1;

-- Use in INSERT
INSERT INTO orders (order_id, revenue)
VALUES (order_seq.NEXTVAL, 500.00);

-- Use in CREATE TABLE
CREATE TABLE orders (
    order_id NUMBER DEFAULT order_seq.NEXTVAL,
    revenue  DECIMAL
);
```

### Key Things to Remember
- Sequences do not guarantee no gaps — if transaction rolls back, number is lost
- Use AUTOINCREMENT or IDENTITY column as simpler alternative:

```
CREATE TABLE orders (
    order_id NUMBER AUTOINCREMENT PRIMARY KEY,
    revenue  DECIMAL
);
```

