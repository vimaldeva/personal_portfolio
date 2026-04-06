import boto3
from strands import Agent, tool
from strands.models import BedrockModel


dynamodb = boto3.client('dynamodb', region_name = 'ap-south-1')

@tool
def get_table_list():
    """ This tool connects to AWS account and returns list of tables in DynamoDB """
    response = dynamodb.list_tables()
    return response.get('TableNames', [])

model_id = "openai.gpt-oss-20b-1:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    tools=[get_table_list],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather." )

response = agent("Tell me list of tables available in dynamoDB")

print(response)