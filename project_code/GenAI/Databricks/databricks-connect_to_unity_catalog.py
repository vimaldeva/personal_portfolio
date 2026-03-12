import pandas as pd
from databricks import sql
import os
from dotenv import load_dotenv
import json

load_dotenv()

connection = sql.connect(
    server_hostname=os.getenv('DATABRICKS_HOST'),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_TOKEN")
)

query = """
select * from retail.silver.dim_product
"""

with connection.cursor() as cursor:
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

connection.close()

# ✅ BEST FOR LLM: records format (array of row objects)
llm_json = df.head(20).to_json(orient='records', indent=2)  # Limit rows + pretty print

print("LLM-Ready JSON:")
print(llm_json)

# Save to file
with open('product_data.json', 'w') as f:
    json.dump(json.loads(llm_json), f, indent=2)

print("\n💾 Saved to product_data.json")
