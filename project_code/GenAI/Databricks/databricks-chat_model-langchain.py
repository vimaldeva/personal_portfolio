from databricks_langchain import ChatDatabricks
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["DATABRICKS_HOST"] = os.getenv("DATABRICKS_HOST") 
os.environ["DATABRICKS_TOKEN"] = os.getenv("DATABRICKS_TOKEN")

chat_model = ChatDatabricks(
    endpoint="databricks-gpt-oss-20b",
    temperature=0.1,
    max_tokens=250,
)
response  = chat_model.invoke("Tell me about Data Engineering")

print(response)
