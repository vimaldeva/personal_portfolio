from openai import OpenAI
import os

# Set your token securely
DATABRICKS_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
databricks_host = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()

BASE_URL = f"{databricks_host}/serving-endpoints"

client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url=BASE_URL
)

response = client.chat.completions.create(
    model="databricks-llama-4-maverick", 
    messages=[
        {"role": "user", "content": "What is an LLM agent?"}
    ]
)

# Print the response
print(response.choices[0].message.content)