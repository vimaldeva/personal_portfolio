from strands.plugins import Plugin, hook
from strands.hooks import BeforeToolCallEvent, AfterModelCallEvent

import boto3
from strands import Agent, tool
from strands.models import BedrockModel


class ModelMonitorPlugin(Plugin):
    name = "model-monitor"

    @hook
    def before_tool(self, event: BeforeToolCallEvent) -> None:
        # Block *any* tool from running
        event.cancel = (
            "Tool use is disabled due to security policy. "
            "I cannot call tools to access DynamoDB."
        )

    @hook
    def on_model_event(self, event: AfterModelCallEvent) -> None:
        print("-------------------------------------------------------------")


dynamodb = boto3.client("dynamodb", region_name="ap-south-1")

@tool
def get_table_list() -> list:
    """This tool connects to AWS account and returns list of tables in DynamoDB"""
    response = dynamodb.list_tables()
    return response.get("TableNames", [])


model = BedrockModel(model_id="openai.gpt-oss-20b-1:0")

agent = Agent(
    model=model,
    tools=[get_table_list],
    plugins=[ModelMonitorPlugin()],
    system_prompt="You're a helpful assistant, but tool use is disabled.",
)

response = agent("Tell me list of dynamodb tables available")
print(response)