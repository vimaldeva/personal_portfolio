## Short Query Acceleration (SQA)

### What is it?
- Redshift predicts which queries will finish quickly and fast-tracks them
- Short queries skip the WLM queue and run in a dedicated SQA slot immediately
- Prevents short queries from waiting behind long-running heavy queries

```
Without SQA:
Short query (0.5 sec) → stuck waiting behind 10 min ETL query → bad experience

With SQA:
Short query (0.5 sec) → detected as short → runs immediately in SQA slot ✅
Long ETL query        → runs normally in WLM queue
```

### Key Things to Remember
- SQA uses ML to predict query execution time before running
- Enabled by default with Automatic WLM
- You can set max SQA execution time (1-20 seconds) — queries predicted under this run in SQA
- Only works for read queries — CREATE, INSERT, COPY not eligible

Check if query used SQA:
```
SELECT query, service_class
FROM stl_wlm_query
WHERE service_class = 14;  -- service class 14 = SQA queue
```