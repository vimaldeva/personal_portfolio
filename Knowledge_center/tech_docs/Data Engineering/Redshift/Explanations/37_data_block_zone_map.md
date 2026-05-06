## Data Blocks and Zone Maps in Redshift

### Data Blocks — What is it?
- The smallest unit of storage in Redshift
- Each column's data is broken into and stored as 1MB blocks on disk
- Redshift reads data block by block — never partial blocks

```
orders table — Salary Column (total 10MB)
├── Block 1 (1MB) → rows 1 to 50,000
├── Block 2 (1MB) → rows 50,001 to 100,000
├── Block 3 (1MB) → rows 100,001 to 150,000
...
└── Block 10 (1MB) → rows 450,001 to 500,000
```

Analogy:

Your column data is a long book
Blocks are the chapters — Redshift reads one chapter at a time
If your answer is in Chapter 3 → it still reads all of Chapter 3, not just one line


### Key Facts About Blocks
- Each block stores data for one column only (columnar)
- Blocks are immutable — once written, never modified in place
- Updates/Deletes = old block marked as ghost row + new block written
- Each block is independently compressed
- A block belongs to one slice on one compute node

---
### Zone Maps — What is it?

- A mini index that Redshift automatically maintains for every block
- Stores MIN and MAX value of each block for every column
- Lives in-memory on the Leader Node — super fast to check
- Used to skip blocks entirely before even reading from disk

```
Salary Column Blocks + Their Zone Maps:

Block 1 → Zone Map: MIN=20000, MAX=45000
Block 2 → Zone Map: MIN=45001, MAX=70000
Block 3 → Zone Map: MIN=70001, MAX=95000
Block 4 → Zone Map: MIN=95001, MAX=120000
```
### How Zone Maps Work During a Query

```
SELECT * FROM employees WHERE salary > 90000;
```

```
Redshift checks Zone Maps FIRST (in memory — instant):

Block 1: MIN=20000, MAX=45000 → MAX < 90000 → SKIP ✅
Block 2: MIN=45001, MAX=70000 → MAX < 90000 → SKIP ✅
Block 3: MIN=70001, MAX=95000 → MAX > 90000 → SCAN 🔍
Block 4: MIN=95001, MAX=120000 → MIN > 90000 → SCAN 🔍

Result: Only 2 out of 4 blocks read from disk → 50% I/O saved
```

Analogy:

Zone Map = Index at the back of a textbook
Instead of reading every page, you check the index first
"Topic X is on pages 200-220" → skip everything else

---

### Zone Maps Work Best With Sort Keys
- Zone Maps are most effective when data is physically sorted on disk
- If salary column is unsorted → MIN/MAX per block overlap → hard to skip blocks
```
UNSORTED salary blocks (zone maps overlap → can't skip much):
Block 1: MIN=20000, MAX=110000  ← wide range, must scan
Block 2: MIN=15000, MAX=105000  ← wide range, must scan
Block 3: MIN=25000, MAX=115000  ← wide range, must scan

SORTED salary blocks (zone maps are tight → skip easily):
Block 1: MIN=20000, MAX=45000   → skip if query > 90000 ✅
Block 2: MIN=45001, MAX=70000   → skip if query > 90000 ✅
Block 3: MIN=70001, MAX=95000   → scan
Block 4: MIN=95001, MAX=120000  → scan
```

This is exactly why Sort Keys exist — to make Zone Maps effective

### Blocks + Zone Maps Together


```
Query Flow:
        ↓
Leader Node checks Zone Maps (in-memory, instant)
        ↓
Identifies which blocks to skip vs scan
        ↓
Only relevant blocks fetched from disk (RMS or SSD cache)
        ↓
Data processed → result returned
```

### Key Things to Remember

| Concept | Key Point |
| :-- | :-- |
| Block size | Fixed at 1MB |
| Zone Map stores | MIN + MAX per block per column |
| Zone Maps live | In-memory on Leader Node |
| Zone Maps are | Automatic — no setup needed |
| Best used with | Sort Keys to avoid overlapping ranges |
| Blocks are | Immutable — updates create new blocks |
| Ghost rows | Old blocks not deleted immediately → need VACUUM |
