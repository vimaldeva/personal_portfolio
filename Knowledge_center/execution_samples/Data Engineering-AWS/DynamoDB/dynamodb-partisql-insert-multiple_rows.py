import boto3
from botocore.exceptions import ClientError

def insert_three_rows_partiql():
    client = boto3.client('dynamodb', region_name='ap-south-1')

    print("Inserting 3 rows using Batch PartiQL...")

    try:
        # We define a list of SQL-like statements
        # Note: Use single quotes for strings ('PHY') and no quotes for numbers (202)
        response = client.batch_execute_statement(
            Statements=[
                {
                    'Statement': "INSERT INTO ExamMarks VALUE {'roll_no': 202, 'subject_cd': 'PHY', 'marks': 75}"
                },
                {
                    'Statement': "INSERT INTO ExamMarks VALUE {'roll_no': 202, 'subject_cd': 'CHEM', 'marks': 82}"
                },
                {
                    'Statement': "INSERT INTO ExamMarks VALUE {'roll_no': 203, 'subject_cd': 'MATH', 'marks': 91}"
                }
            ]
        )

        # Check for errors in individual statements
        # The response contains a list of results for each statement
        for i, result in enumerate(response['Responses']):
            if 'Error' in result:
                print(f"Row {i+1} Failed: {result['Error']['Message']}")
            else:
                print(f"Row {i+1} Inserted Successfully.")

    except ClientError as e:
        print(f"Critical Error: {e}")

if __name__ == '__main__':
    insert_three_rows_partiql()
