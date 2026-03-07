import boto3
from pprint import pprint
dynamodb = boto3.client('dynamodb')

table_description = dynamodb.describe_table(TableName='terraform-lock-table')
# pprint(table_list.get('TableNames'))
pprint(table_description.get("Table"))
