import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
table_name = 'Review100Table'

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
}
def lambda_handler(event, context):
    try:
        #treba movie id i username od korisnika
        path = event['path']
        path_parts = path.split('/')
        movie_id = path_parts[-1]
        username = path_parts[-2]

        # Skeniranje tabele sa filterom na movie_id i username_id
        response = table.query(
            KeyConditionExpression=Key('movie_id').eq(movie_id) & Key('username').eq(username)
        )
        items = response['Items']
        print("Items found:", items)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Query executed successfully.',
                'items': items
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error processing request.',
                'error': str(e)
            })
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