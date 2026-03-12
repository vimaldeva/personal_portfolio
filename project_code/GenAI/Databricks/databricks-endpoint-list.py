
import os
from dotenv import load_dotenv

load_dotenv()


os.environ["DATABRICKS_HOST"] = os.getenv("DATABRICKS_HOST") 
os.environ["DATABRICKS_TOKEN"] = os.getenv("DATABRICKS_TOKEN")

import databricks.sdk
w = databricks.sdk.WorkspaceClient()
endpoints = w.serving_endpoints.list()
for ep in endpoints:
    print(f"Available: {ep.name}")
