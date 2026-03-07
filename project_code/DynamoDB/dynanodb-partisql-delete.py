import boto3
from botocore.exceptions import ClientError
from pprint import pprint

dynamodb_client = boto3.client(
            'dynamodb',
            region_name='ap-south-1'   )

statement_1 = "delete from  ExamMarks where roll_no = 102 AND subject_cd = 'MATH-101'"
dynamodb_client.execute_statement(Statement = statement_1)

# pprint(a.get("Items"))

