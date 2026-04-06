from __future__ import annotations
from typing import Any

from strands import Agent, tool
from strands.plugins import Plugin, hook
from strands.hooks import AfterToolCallEvent
from strands.models import BedrockModel


@tool
def get_customer_record(customer_id: str) -> dict:
    """Demo tool that returns sensitive fields."""
    return {
        "customer_id": customer_id,
        "name": "Aarav Kumar",
        "email": "aarav@example.com",
        "access_token": "SECRET_TOKEN_VALUE",
        "notes": "VIP",
    }


def redact(obj: Any, keys: set[str]) -> Any:
    if isinstance(obj, dict):
        return {k: ("[REDACTED]" if k in keys else redact(v, keys)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(x, keys) for x in obj]
    return obj


class RedactSensitivePlugin(Plugin):
    name = "redact-sensitive"

    def __init__(self):
        super().__init__()
        self.keys = {"email", "phone", "access_token", "password", "ssn"}

    @hook
    def after_tool_call(self, event: AfterToolCallEvent) -> None:
        if event.tool_use["name"] != "get_customer_record":
            return

        # In strands-agents==1.33.0, the tool output is `event.result`
        event.result = redact(event.result, self.keys)


model = BedrockModel(model_id="openai.gpt-oss-20b-1:0")

agent = Agent(
    model=model,
    tools=[get_customer_record],
    plugins=[RedactSensitivePlugin()],
    system_prompt="You are a helpful assistant",
)

agent("Fetch customer 123 and summarize.")