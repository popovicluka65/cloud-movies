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
        ids = path_parts[-1]
        ids_parts = ids.split('++++')
        partition_key = ids_parts[-2]
        subscriber = ids_parts[-1]
        response_delete = table.delete_item(
                Key={
                    'subscription_id': partition_key,
                    'subscriber':subscriber
                }
            )

        print(response_delete)

        return {
                'headers': headers,
                'statusCode': 200,
                'body': json.dumps({'message': f'Deleted item'})
            }
        # else:
        #     return {
        #         'headers': headers,
        #         'statusCode': 404,
        #         'body': json.dumps({'message': f'Id {partition_key} not found'})
        #     }

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
