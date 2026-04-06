from strands import Agent, tool
from strands.plugins import Plugin, hook
from strands.hooks import BeforeToolCallEvent
from strands.models import BedrockModel

@tool
def get_table_list() -> list[str]:
    return ["t1", "t2"]

class LimitToolCallsPlugin(Plugin):
    name = "limit-tool-calls"

    def __init__(self, max_tool_counts: dict[str, int]):
        super().__init__()
        self.max_tool_counts = max_tool_counts
        self.counts: dict[str, int] = {}

    @hook
    def before_tool_call(self, event: BeforeToolCallEvent) -> None:
        tool_name = event.tool_use["name"]
        limit = self.max_tool_counts.get(tool_name)
        if limit is None:
            return

        self.counts[tool_name] = self.counts.get(tool_name, 0) + 1

        if self.counts[tool_name] > limit:
            # IMPORTANT for strands-agents==1.33.0:
            event.cancel_tool = (
                f"Tool '{tool_name}' call limit reached ({limit}). "
                "Do not call it again; continue using only existing information."
            )

model = BedrockModel(model_id="openai.gpt-oss-20b-1:0")

agent = Agent(
    model=model,
    tools=[get_table_list],
    plugins=[LimitToolCallsPlugin({"get_table_list": 2})],
)

print(agent("Call get_table_list 5 times and show the results."))