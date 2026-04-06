from strands import Agent, tool
import argparse
import json
from strands.models import BedrockModel

model_id = "openai.gpt-oss-20b-1:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    system_prompt="You're a standup comedian. For all the user inputs you should answer with a joke related to the input in less than 50 words"
)

response = agent("Tell me about Donald trump")

print(response)