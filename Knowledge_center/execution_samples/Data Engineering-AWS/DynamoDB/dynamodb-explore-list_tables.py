import boto3
from pprint import pprint
dynamodb = boto3.client('dynamodb')

table_list = dynamodb.list_tables(ExclusiveStartTableName='string')
pprint(table_list.get('TableNames'))
