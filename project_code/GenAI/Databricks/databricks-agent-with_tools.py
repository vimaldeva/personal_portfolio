import os
import json
import pandas as pd
from databricks import sql
import mlflow
from dotenv import load_dotenv
# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent

from langchain_databricks import ChatDatabricks
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
# from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# 1. Setup MLflow
mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/Users/vimaldeva10@gmail.com/Sales_analyst_v1")
mlflow.langchain.autolog()

endpoint_name = "databricks-meta-llama-3-3-70b-instruct"

# 2. Setup Model (Use Llama 3 for speed and accuracy)
chat_model = ChatDatabricks(
    endpoint= endpoint_name, # MUCH faster/smarter than gpt-oss-20b
    temperature=0.1,
    max_tokens=500,
)

# 3. Define Tools
@tool
def get_table_metadata(table_name: str) -> str:
    """
    Fetches column names and types for a specific table in the retail.silver schema.
    Input should be the table name (e.g., 'dim_product').
    """
    # Note: In production, consider passing a global connection or connection pool
    try:
        connection = sql.connect(
            server_hostname=os.getenv('DATABRICKS_HOST'),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        
        # Sanitize input to prevent injection (basic example)
        clean_table = table_name.replace(";", "").strip()
        query = f"DESCRIBE retail.silver.{clean_table}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            # Get column name and data type
            df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
            # Keep only relevant columns to save context window
            df = df[['col_name', 'data_type']]

        connection.close()
        return df.to_string(index=False)
    except Exception as e:
        return f"Error fetching metadata: {str(e)}"

@tool
def execute_sql_query(query: str) -> str:
    """
    Executes a SELECT SQL query on Databricks and returns the result.
    Input must be a valid Databricks SQL query string.
    """
    try:
        connection = sql.connect(
            server_hostname=os.getenv('DATABRICKS_HOST'),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            if not results:
                return "Query executed successfully but returned no rows."
            df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
            
        connection.close()
        return df.to_string(index=False)
    except Exception as e:
        return f"Error executing query: {str(e)}"

# 4. Create ONE Agent (Flattened)
tools = [get_table_metadata, execute_sql_query]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Data Analyst. 
    1. First, use 'get_table_metadata' to understand the table structure (default table: retail.silver.dim_product).
    2. Then, construct a valid Databricks SQL query to answer the user's question.
    3. Finally, output ONLY the SQL query. Do not execute it unless asked to fetch data.
    """),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Use tool calling agent (more efficient than ReAct for Llama 3)
agent_executor = create_agent(chat_model, tools)


print("Running Agent...")
response = agent_executor.invoke(
    {"messages": [HumanMessage(content="what is the average price of the product ?")]}
)

# Parse the output (LangGraph returns a list of messages)
print("\n--- RESULT ---")
print(response["messages"][-1].content)
