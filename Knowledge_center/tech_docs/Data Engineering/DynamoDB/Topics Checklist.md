### DynamoDB

- What is DynamoDB ?
- What is is used for ?
- Common use cases
- DynamoDB vs Relational Datatabase (structure, scaling, querying, relationship)
- Advantages/Disadvantages
- DynamoDB vs MongoDB
- DynamoDB vs CosmosDB

---

- Hierarchy Names (Table, item, atttribute)
- Data types
- Keys (partition keys, sort keys)
- Partition keys
- Sort keys
- Composite keys (partition + sort key)
- DynamoDB API (Getitem, Putitem, updateitem, deleteitem)
- Query vs Scan
- Consistent reads (eventual vs strong consistency)
- Secondary Indexes (Global Secondary Index, Local Secondary Index)
- DynamoDB Streams
- DynamoDB Accelerator (DAX)
- DynamoDB Transactions (TransactionWriteItem)
- Batch operations (Batchriteitem, BatchGetItem)
- DynamoDB TTL (Time To Live)
- DynamoDB On-Demand vs Provisioned Capacity
- DynamoDB Auto Scaling
- DynamoDB Global Tables (multi-region replication)
- Capacity Units (Read Capacity Units, Write Capacity Units)
- Capacity Modes (On-Demand, Provisioned)
- Projections (ALL, KEYS_ONLY, INCLUDE)
- DynamoDB Data Modeling (Single Table Design, Access Patterns)
- DynamoDB Best Practices (Indexing, Querying, Scaling)

---

**Scenario1** What is DAX ?

- DynamoDB DAX (DynamoDB Accelerator) is an in-memory caching service that provides fast read performance for DynamoDB tables. It is designed to reduce the latency of read operations by caching frequently accessed data, allowing applications to retrieve data from the cache instead of directly from DynamoDB. DAX can significantly improve the performance of read-heavy workloads, such as those with high read-to-write ratios, by reducing the time it takes to access data.

---

**Scenario2** Tell me about DynamoDB Data Modeling
- DynamoDB Data Modeling is the process of designing the structure of a DynamoDB table to efficiently store and retrieve data based on specific access patterns. Unlike traditional relational databases, DynamoDB uses a NoSQL approach, which requires a different mindset when it comes to data modeling. The key principles of DynamoDB data modeling include: 
1. Single Table Design: Instead of creating multiple tables for different entities, DynamoDB encourages a single table design where all related data is stored in a single table. This allows for efficient querying and reduces the need for complex joins.
2. Access Patterns: Data modeling in DynamoDB is driven by access patterns, which are the specific ways in which applications will access the data. By understanding the access patterns, you can design the table structure and choose appropriate keys to optimize query performance.
3. Keys: Choosing the right partition key and sort key is crucial for efficient data retrieval. The partition key determines how data is distributed across partitions, while the sort key allows for efficient querying and sorting of data within a partition.
4. Secondary Indexes: DynamoDB allows for the creation of secondary indexes (Global Secondary Indexes and Local Secondary Indexes) to enable additional query patterns without affecting the primary key structure.
5. Denormalization: Since DynamoDB does not support joins, denormalization is often used to store related data together in the same item or table. This can improve query performance but may require additional storage and maintenance.

Overall, DynamoDB data modeling requires careful consideration of the access patterns and the trade-offs between performance and storage efficiency to design a schema that meets the application's needs.

---

#### DynamoDB Best Practices (Indexing, Querying, Scaling)
- Indexing: Use secondary indexes (Global Secondary Indexes and Local Secondary Indexes) to enable additional query patterns and improve query performance. However, be mindful of the additional storage costs and write capacity units associated with indexes.
- Querying: Use the Query operation instead of Scan whenever possible, as it is more efficient and allows you to retrieve specific items based on the partition key and sort key. Use filters to further narrow down results after querying.
- Scaling: Use Auto Scaling to automatically adjust the provisioned capacity of your DynamoDB tables based on traffic patterns. Consider using On-Demand capacity mode for unpredictable workloads or when you want to avoid managing capacity. Monitor your tables' performance and adjust capacity as needed to ensure optimal performance and cost efficiency.   
- Data Modeling: Design your DynamoDB tables based on access patterns and consider using a single table design to optimize query performance. Choose appropriate partition keys and sort keys to ensure efficient data distribution and retrieval. 
- Caching: Consider using DynamoDB Accelerator (DAX) for read-heavy workloads to reduce latency and improve performance. DAX can significantly speed up read operations by caching frequently accessed data in memory.
- Error Handling: Implement error handling and retry logic in your application to handle transient errors and ensure data consistency. Use exponential backoff for retries to avoid overwhelming the DynamoDB service during high traffic periods.
- Security: Use AWS Identity and Access Management (IAM) to control access to your DynamoDB tables and ensure that only authorized users and applications can access your data. Consider using encryption at rest and in transit to protect sensitive data stored in DynamoDB.

--- 

#### DynamoDB Autoscaling

DynamoDB Auto Scaling is a feature that automatically adjusts the provisioned capacity of your DynamoDB tables based on traffic patterns. It helps ensure that your tables can handle varying workloads without manual intervention, while also optimizing costs by scaling down during periods of low traffic. Auto Scaling uses CloudWatch alarms to monitor the utilization of your tables and triggers scaling actions when certain thresholds are met. You can configure Auto Scaling to maintain a target utilization percentage for your tables, allowing you to balance performance and cost effectively.

---
#### DynamoDB multi region tables
DynamoDB Global Tables is a feature that allows you to create multi-region, fully replicated tables in DynamoDB. This means that you can have copies of your DynamoDB tables in multiple AWS regions, providing low-latency access to data for users around the world and improving availability and fault tolerance. Global Tables automatically replicate data across regions, ensuring that changes made to one table are propagated to all other replicas. This allows for seamless read and write operations across regions, making it easier to build globally distributed applications with DynamoDB.