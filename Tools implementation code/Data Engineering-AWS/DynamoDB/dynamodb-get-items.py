import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer

# Helper to convert DynamoDB format -> Python format
# e.g. {'S': 'Rahul'} -> 'Rahul'
deserializer = TypeDeserializer()

def deserialize_item(item):
    return {k: deserializer.deserialize(v) for k, v in item.items()}

def fetch_exam_data():
    client = boto3.client('dynamodb', region_name='ap-south-1')
    table_name = 'ExamMarks'

    # ==========================================
    # 1. GET_ITEM: Fetch a SINGLE specific record
    # ==========================================
    print("\n--- 1. Get Item (Specific Student & Subject) ---")
    try:
        response = client.get_item(
            TableName=table_name,
            Key={
                'roll_no': {'N': '101'}  ,       # Partition Key
                'subject_cd': {'S': 'MATH-101'}   # Sort Key
            }
        )

        if 'Item' in response:
            # Convert low-level format to normal python dict
            item = deserialize_item(response['Item'])
            print(f"Found Record: {item}")
        else:
            print("No item found with that key.")

    except ClientError as e:
        print(f"Error: {e}")

    # ==========================================
    # 2. QUERY: Fetch ALL subjects for ONE Student
    # ==========================================
    print("\n--- 2. Query (All exams for Roll No 101) ---")
    try:
        response = client.query(
            TableName=table_name,
            # Condition: roll_no MUST equal :r
            KeyConditionExpression='roll_no = :r',
            # Define what :r is
            ExpressionAttributeValues={
                ':r': {'N': '101'}
            }
        )

        items = response.get('Items', [])
        print(f"Found {len(items)} exams for student 101:")
        for raw_item in items:
            item = deserialize_item(raw_item)
            print(f" - {item['subject_cd']}: {item['marks']} marks")

    except ClientError as e:
        print(f"Error: {e}")

    # ==========================================
    # 3. SCAN: Fetch EVERYTHING in the table
    # ==========================================
    print("\n--- 3. Scan (All Data) ---")
    try:
        response = client.scan(TableName=table_name)
        
        items = response.get('Items', [])
        for raw_item in items:
            item = deserialize_item(raw_item)
            print(f" - Roll: {item['roll_no']}, Subject: {item['subject_cd']}, Name: {item.get('student_name')}")

    except ClientError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fetch_exam_data()
