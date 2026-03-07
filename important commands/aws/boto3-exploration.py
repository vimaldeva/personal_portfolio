import boto3
from pprint import pprint
dynamodb = boto3.client('dynamodb')
# table = dynamodb.Table('Movies')

pprint(dir(dynamodb))
help(dynamodb.create_table)
