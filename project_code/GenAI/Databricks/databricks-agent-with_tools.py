from databricks_langchain import ChatDatabricks
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
import pandas as pd
from databricks import sql
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import mlflow

import langchain.agents
from langchain.agents import create_agent

import os

load_dotenv()

mlflow.set_tracking_uri("databricks")

experiment_path = "/Users/vimaldeva10@gmail.com/Sales_analyst_v1"
mlflow.set_experiment(experiment_path)

mlflow.openai.autolog()


os.environ["DATABRICKS_HOST"] = os.getenv("DATABRICKS_HOST") 
os.environ["DATABRICKS_TOKEN"] = os.getenv("DATABRICKS_TOKEN")

chat_model = ChatDatabricks(
    # endpoint="databricks-meta-llama-3-3-70b-instruct",
    endpoint="databricks-gpt-oss-20b",
    temperature=0.1,
    max_tokens=250,
)

@tool
def get_table_metadata() -> str:
    """ use this tool to fetch metadata information about the unity catalog"""
    query = """
    describe retail.silver.dim_product
    """

    connection = sql.connect(
        server_hostname=os.getenv('DATABRICKS_HOST'),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN")
    )

    query = """
    describe retail.silver.dim_product
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

    connection.close()

    llm_text = df.to_string(index=False, justify='left')
    
    return llm_text

    # - You should send the framed SQL query as input to the get_athena_query_result tool. The input of this tool should strictly contain only SQL query. Nothing more, nothing less.
    # - Execute the get_athena_query_result tool and send back/display the results as output. You dont need to add anything addition to this.

@tool
def execute_query(query : str) -> str:
    """ This tool is used to connect to Databricks SQL warehouse and execute a query there"""
    connection = sql.connect(
        server_hostname=os.getenv('DATABRICKS_HOST'),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN")
    )

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])

    connection.close()

    llm_text = df.to_string(index=False, justify='left')  
    
    return llm_text


sql_agent_prompt = """
<RoleDescription>
You are an Expert SQL Developer who helps to frame SQL queries for a given requirement/use case and execute the queries and send back the result. You should make use of the tools available to get necessary table information and frame SQL query for the given requirement and send back the SQL query as output. The SQL queries will be run on Databricks SQL warehouse, so the SQL queries should be compatible for Databricks SQL warehouse.
</RoleDescription>
<TableDetails>
    catalog_name : retail
    schema_name : silver
    table_name : dim_product
    sample_query : select * from  retail.silver.dim_product
</TableDetails>
<Tools>
    - get_table_metadata : This tool is used to get table metadata from Databricks unity catalog.
</Tools>
<ExecutionSteps>
You should follow the following instructions in give order without Fail.
    - You will get a requirement as an input to this SQl Developer Agent.
    - Use the get_table_metadata tool to get metadata information of the tables in Databricks unity catalog.
    - Based on the metadata information available, you should frame an SQL query in Databricks SQL warehouse compatible format to get necessary information that was requested in the input question.
    - You shoulkd query only a maximum of 99 rows. So frame the queries accordingly. Also query only the necessary columns and avoid querying unnecessary columns to save cost. Once the query is framed, send the SQL query back as output
</ExecutionSteps>
<OutOfScope>
    - Your role is a Data/SQL Developer and you should only accept inputs that involves framingn queries and getching back data to the user.
    - Do not answer any questions that is outside the scope of SQL/Data Analyst.
</OutOfScope>
<OutputFormat>
Your output should only have SQL query as output. Nothing more, nothing less. Avoid mentioning anything additional in the output.
</OutputFormat>

"""

agent = create_agent(chat_model, 
                     tools = [get_table_metadata],
                     system_prompt = sql_agent_prompt)


result = agent.invoke(
    {"messages": [HumanMessage("Number of distinct products avaulable")]} )

ai_message = result['messages'][-1]
content = ai_message.content
def safe_databricks_parse(content: str):
    """Parse Databricks structured responses safely."""
    if not content or content.strip() == '':
        return "No response generated."
    
    try:
        data = json.loads(content)
        if isinstance(data, list):
            # Find text block
            for item in data:
                if isinstance(item, dict) and item.get('type') == 'text':
                    return item['text']
            return json.dumps(data, indent=2)  # Pretty print full JSON
        return str(data)
    except:
        return content.strip()

print(safe_databricks_parse(content))
