import boto3
from botocore.exceptions import ClientError

def insert_exam_marks():
    # 1. Initialize the Client
    # NOTE: If you are running locally, uncomment the endpoint_url line.
    # If you are connecting to real AWS, keep it commented out.
    dynamodb_client = boto3.client(
        'dynamodb',
        region_name='ap-south-1',
    )

    table_name = 'ExamMarks'

    print(f"Inserting records into '{table_name}'...")

    try:
        # --- Record 1: Math Exam ---
        # roll_no (Partition Key) = 101
        # subject_cd (Sort Key) = MATH-101
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'roll_no': {'N': '101'},         # 'N' for Number (Value must be a string)
                'subject_cd': {'S': 'MATH-101'}, # 'S' for String
                'marks': {'N': '85'},            # Attribute: Marks
                'student_name': {'S': 'Rahul'},  # Attribute: Name
                'pass_status': {'BOOL': True}    # Attribute: Boolean
            }
        )
        print("Inserted: Rahul - MATH-101")

        # --- Record 2: Physics Exam (Same Student, Different Subject) ---
        # roll_no = 101
        # subject_cd = PHY-102
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'roll_no': {'N': '101'},
                'subject_cd': {'S': 'PHY-102'},
                'marks': {'N': '78'},
                'student_name': {'S': 'Rahul'},
                'lab_completed': {'BOOL': True}
            }
        )
        print("Inserted: Rahul - PHY-102")

        # --- Record 3: Different Student ---
        # roll_no = 102
        # subject_cd = MATH-101
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'roll_no': {'N': '102'},
                'subject_cd': {'S': 'MATH-101'},
                'marks': {'N': '92'},
                'student_name': {'S': 'Priya'},
                'remarks': {'S': 'Excellent performance'}
            }
        )
        print("Inserted: Priya - MATH-101")

    except ClientError as e:
        print(f"Error inserting item: {e}")

if __name__ == '__main__':
    insert_exam_marks()
