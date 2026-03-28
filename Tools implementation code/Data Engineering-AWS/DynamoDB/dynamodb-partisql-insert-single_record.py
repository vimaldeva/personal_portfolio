import boto3
from botocore.exceptions import ClientError
from pprint import pprint

dynamodb_client = boto3.client(
            'dynamodb',
            region_name='ap-south-1'   )

statement_1 = "INSERT INTO ExamMarks VALUE {'roll_no': 200, 'subject_cd': 'PHY'}"
dynamodb_client.execute_statement(Statement = statement_1)

# pprint(a.get("Items"))

