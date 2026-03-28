import boto3
from botocore.exceptions import ClientError

def create_table_with_client():
    # 1. Initialize the Client
    # Note: We use 'client' instead of 'resource'
    dynamodb_client = boto3.client(
        'dynamodb',
        region_name='ap-south-1'
    )

    table_name = 'ExamMarks'

    print(f"Creating table '{table_name}' using Client...")

    try:
        # 2. Call create_table
        # The client returns a dictionary containing the API response
        response = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'roll_no',
                    'KeyType': 'HASH'  # Partition Key
                },
                {
                    'AttributeName': 'subject_cd',
                    'KeyType': 'RANGE' # Sort Key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'roll_no',
                    'AttributeType': 'N' # String
                },
                {
                    'AttributeName': 'subject_cd',
                    'AttributeType': 'S' # String
                },
            ],
            BillingMode= 'PAY_PER_REQUEST'
        )
        
        print("Create request sent. Waiting for table to exist...")

        # 3. Use a Waiter
        # Since 'client' is low-level, it doesn't have .wait_until_exists() directly on the table.
        # We must create a waiter object explicitly.
        waiter = dynamodb_client.get_waiter('table_exists')
        
        # This will poll the table status every 20 seconds (default) until it is ACTIVE
        waiter.wait(TableName=table_name)

        print(f"Success! Table '{table_name}' is now ACTIVE.")
        
        # 4. Inspect the response (Optional)
        # This shows you the raw JSON structure AWS returns
        print("\nRaw Response Description:")
        print(response['TableDescription']['TableStatus'])

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Error: The table '{table_name}' already exists.")
        else:
            print(f"Unexpected error: {e}")

if __name__ == '__main__':
    create_table_with_client()
