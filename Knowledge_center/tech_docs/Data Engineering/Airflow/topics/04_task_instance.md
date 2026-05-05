## Task Instance
- A single execution of a Task in a specific DAG Run
- Think of it as Task + DAG Run combined
- Tracks the state of each task execution separately
- States → Queued / Running / Success / Failed / Skipped / Up for Retry

```
DAG Run Jan 1
├── extract_task   → ✅ Success
├── transform_task → ✅ Success
└── load_task      → ❌ Failed

DAG Run Jan 2
├── extract_task   → ✅ Success
├── transform_task → ⏳ Running
└── load_task      → 🔲 Queued
```