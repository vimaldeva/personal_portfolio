import asyncio
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient 
from mcp import stdio_client, StdioServerParameters 

# Initialize the Bedrock Model
model_id = "openai.gpt-oss-20b-1:0"
model = BedrockModel(model_id=model_id)

async def main():
    # 1. Wrap the transport parameters inside an MCPClient using a lambda function
    mcp_client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="python",
                args=["server.py"]
            )
        )
    )

    # 2. Open using a standard synchronous 'with' block
    with mcp_client:
        
        # 3. Pull the tools from the active server session
        weather_tools = mcp_client.list_tools_sync() 

        # 4. Initialize the Agent with the proper system prompt
        agent = Agent(
            model=model,
            system_prompt=(
                "You are a Weather Assistant. "
                "Your goal is to help users find accurate weather information using the provided tools."
            ),
            tools=weather_tools
        )

        # 5. EXECUTION FIX: Call the agent directly as a function (No .run() and no await)
        result = agent("What is the weather like in New York?")
        
        # 6. Access the textual string content returned by Strands
        print(f"Agent Response: {result}")

if __name__ == "__main__":
    asyncio.run(main())
