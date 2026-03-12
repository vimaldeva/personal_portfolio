from databricks_langchain import ChatDatabricks
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json

import langchain.agents
from langchain.agents import create_agent

import os
from dotenv import load_dotenv

load_dotenv()


os.environ["DATABRICKS_HOST"] = os.getenv("DATABRICKS_HOST") 
os.environ["DATABRICKS_TOKEN"] = os.getenv("DATABRICKS_TOKEN")

chat_model = ChatDatabricks(
    # endpoint="databricks-meta-llama-3-3-70b-instruct",
    endpoint="databricks-gpt-oss-20b",
    temperature=0.1,
    max_tokens=250,
)

system_prompt = "You are a standup comedian . For all the questions that is being asked, you should answer saracastically to that topic in less than 100 words."
agent = create_agent(chat_model, system_prompt = system_prompt)


result = agent.invoke(
    {"messages": [HumanMessage("Tell me about cricket.")]} )

ai_message = result['messages'][-1]

print(json.loads(result['messages'][-1].content)[1]['text'])

