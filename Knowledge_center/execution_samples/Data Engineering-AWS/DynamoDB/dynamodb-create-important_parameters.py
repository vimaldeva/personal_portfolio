import boto3
from botocore.exceptions import ClientError

def create_robust_table():
    dynamodb_client = boto3.client('dynamodb', region_name='ap-south-1')
    table_name = 'ExamMarks'

    print(f"Creating table '{table_name}'...")

    try:
        response = dynamodb_client.create_table(
            TableName=table_name,
            # 1. BILLING
            BillingMode='PAY_PER_REQUEST',

            # 2. KEY SCHEMA (Primary Key)
            KeySchema=[
                {'AttributeName': 'roll_no', 'KeyType': 'HASH'},    # Partition Key
                {'AttributeName': 'subject_cd', 'KeyType': 'RANGE'} # Sort Key
            ],

            # 3. ATTRIBUTE DEFINITIONS
            # IMPORTANT: You must define the types for Primary Keys AND GSI Keys here.
            AttributeDefinitions=[
                {'AttributeName': 'roll_no', 'AttributeType': 'N'},
                {'AttributeName': 'subject_cd', 'AttributeType': 'S'},
                {'AttributeName': 'student_name', 'AttributeType': 'S'} # <--- Added for GSI
            ],

            # 4. GLOBAL SECONDARY INDEXES (GSIs)
            # Allows you to query by 'student_name' efficiently
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'StudentNameIndex',
                    'KeySchema': [
                        {'AttributeName': 'student_name', 'KeyType': 'HASH'},
                        # You can optionally add a sort key here too
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL' # Copies all attributes to the index (easiest, but more storage)
                        # Options: 'KEYS_ONLY', 'INCLUDE', 'ALL'
                    }
                }
            ],

            # 5. STREAM SPECIFICATION (For Lambda Triggers)
            StreamSpecification={
                'StreamEnabled': True,
                'StreamViewType': 'NEW_AND_OLD_IMAGES' 
                # Options: 'KEYS_ONLY', 'NEW_IMAGE', 'OLD_IMAGE', 'NEW_AND_OLD_IMAGES'
            },

            # 6. TAGS (For Cost Allocation)
            Tags=[
                {'Key': 'Project', 'Value': 'UniversityExamSystem'},
                {'Key': 'Environment', 'Value': 'Production'}
            ],

            # 7. DELETION PROTECTION (Safety)
            # If True, you cannot delete this table until you update settings to False.
            DeletionProtectionEnabled=True
        )
        
        print("Request sent. Waiting for table...")
        waiter = dynamodb_client.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        print("Table created successfully!")

    except ClientError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_robust_table()



-------------------------------------------------------------------------------------------------------

1. Global Secondary Indexes (GSIs) - Most Important
Why: Currently, you can only query efficiently by roll_no. If you want to query by student_name (e.g., "Find all exams for Rahul"), you cannot do it efficiently without a GSI. Requirement: You must add the new key column to AttributeDefinitions.

2. Tags
Why: Essential for AWS billing and organization. You can track how much this specific table costs in the AWS Cost Explorer.

3. StreamSpecification
Why: If you want to trigger a Lambda function every time a record is inserted or updated (e.g., to send an email when marks are uploaded), you need to enable Streams.

4. DeletionProtectionEnabled
Why: Prevents you (or a script) from accidentally deleting the table. You must explicitly disable this setting before you can run delete_table.

  
