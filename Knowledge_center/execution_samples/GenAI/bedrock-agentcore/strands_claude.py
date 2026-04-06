from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
import argparse
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel

app = BedrockAgentCoreApp()

# Create a custom tool 
@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"


model_id = "openai.gpt-oss-20b-1:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather." )

def extract_text_from_response(resp) -> str:
    # Best-case: some SDKs expose .text
    text = getattr(resp, "text", None)
    if isinstance(text, str) and text:
        return text

    msg = getattr(resp, "message", None)
    if isinstance(msg, dict):
        content = msg.get("content", [])
        parts = []
        for item in content:
            # Common shape: {"type": "text", "text": "..."}
            if isinstance(item, dict) and item.get("type") == "text" and "text" in item:
                parts.append(item["text"])
            # Fallback: if "text" exists directly
            elif isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
        if parts:
            return "\n".join(parts)

    # Last resort: stringify the whole response for debugging
    return str(resp)


@app.entrypoint
def strands_agent_bedrock(payload):
    """
    Invoke the agent with a payload
    """
    user_input = payload.get("prompt")
    print("User input:", user_input)
    response = agent(user_input)
    return extract_text_from_response(response)

if __name__ == "__main__":
    app.run()