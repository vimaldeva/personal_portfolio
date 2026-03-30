import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='us-east-1')
payload = json.dumps({"prompt": "what is the previous question that I asked you >"})

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:918524300659:runtime/strands_v2-lJgonv9Lp8',
    runtimeSessionId='123456789012345678901234567890123', # Must be 33+ char. Every new SessionId will create a new MicroVM
    payload=payload
    # qualifier="<Replace with your Endpoint>" # This is Optional. When the field is not provided, Runtime will use DEFAULT endpoint
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)