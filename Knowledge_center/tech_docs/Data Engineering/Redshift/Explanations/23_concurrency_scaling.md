## Concurrency Scaling

### What is it?
- When your main cluster is overwhelmed with queries → Redshift automatically adds temporary cluster capacity
- Extra clusters spin up, handle overflow queries, then spin down when load drops

```
Normal load  → Main cluster handles all queries
Peak load    → Extra queries routed to concurrency scaling clusters
Load drops   → Extra clusters removed automatically
```

### Key Things to Remember
- You pay per second of concurrency scaling cluster usage
- First 1 hour per day is free (accumulates credits)
- Only works with RA3 nodes and Redshift Serverless
- Enable at cluster level — works automatically with WLM queues
- Read queries benefit most — write queries don't scale with this