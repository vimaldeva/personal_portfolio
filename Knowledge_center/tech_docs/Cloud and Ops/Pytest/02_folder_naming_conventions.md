## Folder / Directory Naming Conventions

```
project_root/
│
├── src/                        ← source code (lowercase)
│   ├── transformations/        ← feature-based grouping
│   │   ├── __init__.py
│   │   ├── customer_transform.py
│   │   ├── sales_transform.py
│   │   └── utils.py
│   │
│   └── pipelines/
│       ├── __init__.py
│       └── etl_pipeline.py
│
├── tests/                      ← all tests here (lowercase)
│   ├── conftest.py             ← session-level shared fixtures
│   │
│   ├── unit/                   ← unit tests folder
│   │   ├── conftest.py
│   │   ├── test_customer.py
│   │   └── test_sales.py
│   │
│   ├── integration/            ← integration tests folder
│   │   ├── conftest.py
│   │   └── test_pipeline.py
│   │
│   └── e2e/                    ← end-to-end tests folder
│       └── test_full_flow.py
│
├── data/                       ← test data files
│   ├── input/
│   │   └── sample_customers.csv
│   └── expected/
│       └── expected_output.csv
│
├── conftest.py                 ← root conftest (optional)
├── pytest.ini
├── requirements.txt
└── README.md
```

```
📌 Rules:
  - All lowercase
  - Use underscores for multi-word names
  - Mirror src/ structure in tests/ folder
  - Group by feature or test type
```