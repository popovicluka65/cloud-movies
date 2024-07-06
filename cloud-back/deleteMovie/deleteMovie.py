import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from boto3.dynamodb.conditions import Key  # Dodaj ovaj import

dynamodb = boto3.resource('dynamodb')
table_name = 'Subscription100Table'
table = dynamodb.Table(table_name)
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE',
    'Access-Control-Allow-Headers': 'Content-Type'
}
def lambda_handler(event, context):
    try:
        path = event['path']
        path_parts = path.split('/')
        partition_key = path_parts[-1]
        print(partition_key)
        return {
            'headers': headers,
            'statusCode': 200
        }
    except NoCredentialsError:
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'message': 'Credentials not available'})
        }
    except PartialCredentialsError:
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'message': 'Incomplete credentials provided'})
        }
    except Exception as e:
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }