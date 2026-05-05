## Metadata Database
- The heart of Airflow's state management
- Stores everything →
    - DAG definitions
    - DAG Runs
    - Task Instances and their states
    - Variables
    - Connections
    - XComs
- Default → SQLite (dev only)
- Production → PostgreSQL or MySQL
- Scheduler, Webserver, Workers all read/write from this DB

