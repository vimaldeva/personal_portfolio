
#  %pip install --upgrade strands-agents 
#  dbutils.library.restartPython()

from strands import Agent, tool
from strands.models.openai import OpenAIModel

DATABRICKS_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
databricks_host = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()

BASE_URL = f"{databricks_host}/serving-endpoints"

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

agent = Agent(
    model=databricks_model_provider,
    tools=[calculate_tax, get_company_status]
)

query = "Tell me a joke about cricket"
response = agent(query)
response
