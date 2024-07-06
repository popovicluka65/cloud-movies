import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
table_name = 'Subscription100Table'
table = dynamodb.Table(table_name)
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
}
def lambda_handler(event, context):
    try:
        path = event['path']
        path_parts = path.split('/')
        partition_key = path_parts[-1]

        # Provera da li korisnik postoji pre brisanja
        response = table.query(
            KeyConditionExpression=Key('subscription_id').eq(partition_key)
        )

        if response['Items']:
            # Ako korisnik postoji, izbriši ga
            response_delete = table.delete_item(
                Key={
                    'subscriber': username
                }
            )

            return {
                'headers': headers,
                'statusCode': 200,
                'body': json.dumps({'message': f'Deleted item'})
            }
        else:
            return {
                'headers': headers,
                'statusCode': 404,
                'body': json.dumps({'message': f'Id {partition_key} not found'})
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
