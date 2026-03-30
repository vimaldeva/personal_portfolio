import boto3

client = boto3.client('bedrock-agentcore-control')

response = client.update_agent_runtime(
    agentRuntimeId='strands_v2-lJgonv9Lp8',
    roleArn='arn:aws:iam::918524300659:role/AmazonBedrockAgentCoreSDKRuntime-us-east-1-bfa4111983',
    networkConfiguration={'networkMode': 'PUBLIC'},
    agentRuntimeArtifact={
        'containerConfiguration': {
            'containerUri': '918524300659.dkr.ecr.us-east-1.amazonaws.com/bedrock-agentcore-strands_v2:latest'
        }
    },
    lifecycleConfiguration={
        'idleRuntimeSessionTimeout': 180,  # 30 minutes
        'maxLifetime': 300               # 4 hours
    }
)

print(f"Update started. New Version: ")
