from strands import Agent, tool
from strands.models.openai import OpenAIModel
import mlflow
import json
from typing import List, Dict, Optional

EXPERIMENT_NAME = "/Workspace/Users/vimaldeva10@gmail.com/strands-tax-agent"

mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.strands.autolog()

class DatabricksOpenAIModel(OpenAIModel):
    def format_request(self, *args, **kwargs):
        request = super().format_request(*args, **kwargs)
        request.pop("stream_options", None)
        return request

@tool
def calculate_tax(revenue: float, rate: float = 0.15) -> float:
    """
    Calculates corporate tax on given revenue. Use this tool whenever the user
    asks financial tax questions or requests tax math calculations.
    """
    return revenue * rate

@tool
def get_company_status(company_name: str) -> str:
    """Retrieves the registration and compliance standing for a target enterprise."""
    return f"Company '{company_name}' is active, compliant, and in good standing."

databricks_model_provider = DatabricksOpenAIModel(
    model_id="databricks-llama-4-maverick",
    client_args={
        "api_key": DATABRICKS_TOKEN,
        "base_url": f"{databricks_host}/serving-endpoints"
    },
    params={
        "stream": True
    }
)

def load_history(session_id: str) -> List[Dict]:
    # Replace with durable storage read (e.g. Delta table, Redis, S3)
    return []

def save_history(session_id: str, messages: List[Dict]) -> None:
    # Replace with durable storage write
    pass

def build_agent(history: Optional[List[Dict]] = None) -> Agent:
    agent = Agent(
        model=databricks_model_provider,
        tools=[calculate_tax, get_company_status]
    )
    if history:
        agent.messages = history
    return agent

def chat(session_id: str, user_id: str, query: str):
    history = load_history(session_id)
    agent = build_agent(history)

    with mlflow.start_span(name="chat_turn") as span:
        mlflow.update_current_trace(tags={
            "session_id": session_id,
            "user_id": user_id,
            "app": "strands_databricks_agent"
        })
        span.set_inputs({
            "session_id": session_id,
            "user_id": user_id,
            "query": query,
            "history_length": len(history)
        })

        response = agent(query)

        span.set_outputs({
            "response": str(response)
        })

    save_history(session_id, agent.messages)
    return {
        "session_id": session_id,
        "user_id": user_id,
        "response": str(response),
        "messages": agent.messages
    }


result = chat(
    session_id="session-abc-123",
    user_id="user-vimal",
    query="Tell me a joke about football"
)