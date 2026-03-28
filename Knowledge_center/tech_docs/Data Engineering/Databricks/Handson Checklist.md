# Databricks Hands-On Checklist

##  Notebooks
-  Create notebook
- switch between python and sql between notebooks
- display and visualize using graph in notebook
- check the version hitory in notebook
- use the notebook code in Databricks jobs
- Transfer the notebook code to python file and use it in notebook

## Magic commands

- %sql — Run SQL queries
- %python — Switch to Python
- %md — Render Markdown
- %fs — Interact with Databricks File System
- %run — Run another notebook
- %pip — Install Python packages
- %sh — Run shell commands

## dbutils
`dbutils` is a utility library in Databricks for managing files, secrets, jobs, widgets, and more.  


##### 1. File System Utilities (`dbutils.fs`)


  ```python
  dbutils.fs.ls("/path")
  dbutils.fs.cp("/source", "/destination", recurse=True)
  dbutils.fs.mv("/source", "/destination", recurse=True)
  dbutils.fs.rm("/path", recurse=True)
  dbutils.fs.mkdirs("/path")
  dbutils.fs.head("/path/file.txt", maxBytes=1024)
  dbutils.fs.put("/path/file.txt", "content", overwrite=True)
  ```
##### 2. Secret Management (`dbutils.secrets`)

  ```python
  dbutils.secrets.listScopes()
  dbutils.secrets.get(scope="scope_name", key="key_name")
  dbutils.secrets.list("scope_name")
  ```
##### 3.Widgets Utilities (dbutils.widgets)
```
dbutils.widgets.text("name", "default")
dbutils.widgets.dropdown("name", "default", ["option1", "option2"])
dbutils.widgets.combobox("name", "default", ["option1", "option2"])
dbutils.widgets.multiselect("name", "default", ["option1", "option2"])
dbutils.widgets.get("name")
dbutils.widgets.remove("name")
dbutils.widgets.removeAll()
dbutils.widgets.getArgument("name", "default")
```

##### 4.Notebook Utilities (dbutils.notebook)
```
dbutils.notebook.run("notebook_path", timeout_seconds, {"param":"value"})
dbutils.notebook.exit("return_value")
```

##### 5. Jobs Utilities (dbutils.jobs)
```
dbutils.jobs.exit("message")
```

##### 6.Help Utilities (dbutils.help)
```
dbutils.help()
dbutils.fs.help()
dbutils.secrets.help()
```

## Unity Catalog
- Navigate to unity catalog
- Create catalog, schema and table 
- Automatically scan tables in the catalog and tag columns that contain sensitive data. (this option available in Unity catalog)
- Grant or revoke privilege on catalog level, schema level and table level
- Assign which workspace have access to a given Unity catalog
- Add tags to catalog, schema and table
- Data Quality Monitoring and Anamoly detection feature in schema level and table level
- View column metadata and column sample data
- View version history of the table and what changes is done in each version for delta tables
- View lineage information of tables
- Register GenAI models in unity catalog

- View complete details of the table such as 
```
Properties
delta: 
checkpoint.writeStatsAsJson: "false"
checkpoint.writeStatsAsStruct: "true"
enableDeletionVectors: "true"
enableRowTracking: "true"
feature.appendOnly: "supported"
feature.deletionVectors: "supported"
feature.domainMetadata: "supported"
feature.invariants: "supported"
feature.rowTracking: "supported"
lastCommitTimestamp: "1774019128000"
lastUpdateVersion: "0"
minReaderVersion: "3"
minWriterVersion: "7"
parquet.compression.codec: "zstd"
rowTracking.materializedRowCommitVersionColumnName: "_row-commit-version-col-255b356d-9e92-44f2-b36f-376495ab7a80"
rowTracking.materializedRowIdColumnName: "_row-id-col-304fa995-d732-4e04-9283-85617378a887"
```

## Databricks Jobs
- Create job

#### Tasks
- create different task type like Notebook, python script, SQL query, SQL file, Ingestion pipeline, Declarative pipeline, DBT, Power BI, Dashboard, SQL alert
- Create a SQL query task
- Create a SQL file task
- Create a Notebook task
- Create a python file task
- Add notification to the task
- Add retries for the task
- Set maximum threshold metrics like run duration to the task
- Run the job normally
- Run the job with backfill
- Run the job with different parameters
- View the job run metrics
- View the full job run history

#### Job configurations
- Job notifications
- Different trigger types : Scheduled, File arrival, Table update, Continuos
- Schedule trigger based on timing and Frequency
- File arrival trigger on a certain S3 bucket path or DBFS
- Table update trigger on a given catalog.schema.table 
- Continuous trigger ensures that the job is always active . A new run is started as soon as the previous run is finished.
- Select compute : serverles or a predefined cluster
- Add job parameters as key value pairs
- For multiple taks, you can set dependency on the task as All successded, all completed, atlteast one successded etc.
- You can set maximum concurrent run as 1 or more.
```
# Notebook cell 1: define widgets
dbutils.widgets.text("param1", "default_value", "Parameter 1")
dbutils.widgets.text("param2", "default_value", "Parameter 2")

# Notebook cell 2: fetch widget values
param1_value = dbutils.widgets.get("param1")
param2_value = dbutils.widgets.get("param2")

# Print to confirm
print(f"Param 1: {param1_value}")
print(f"Param 2: {param2_value}")
```

#### Jobs - points to remember
- Jobs can have multiple tasks.
- Jobs does not allow dependency between two jobs like we have in Airflow. You have to mention in tasks for them to run on dependency.
- ``` dbutils.jobs.taskValues ```  , you can use this for similar functionalities like xcom pull and push

```  
In an upstream task: dbutils.jobs.taskValues.set(key="row_count", value=str(count)).
Downstream task: dbutils.jobs.taskValues.get(taskKey="upstream_task_name", key="row_count"). Max payload ~10 KB, string only.

```
- Conditional branching - Databricks Workflows don’t support fully dynamic DAGs
- dbutils are available only in notebook. You cannot use them in python script. You can use the following script for python script 
```
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--param1", default="default")
args = parser.parse_args()

print(args.param1)
```





