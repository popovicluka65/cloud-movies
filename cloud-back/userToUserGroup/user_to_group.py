import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
user_pool_id = 'eu-central-1_0OImNFX7r'
client = boto3.client('cognito-idp', region_name='eu-central-1')

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
}

def lambda_handler(event, context):
    body = json.loads(event['body'])
    try:
        print("Received event:", json.dumps(event))
        body = json.loads(event['body'])
        username = body['username']
        permanent_password = body['password']

        # # Create a new user
        # response = client.admin_create_user(
        #      UserPoolId=user_pool_id,
        #      Username=username,
        #      UserAttributes=user_attributes,
        #      MessageAction='SUPPRESS'
        # )

        # # Set the permanent password for the new user
        response = client.admin_set_user_password(
             UserPoolId=user_pool_id,
             Username=username,
             Password=permanent_password,
             Permanent=True
        )

        response = client.admin_add_user_to_group(
             UserPoolId=user_pool_id,
             Username=username,
             GroupName='user'
        )
        return {
            'headers': headers,
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Add user to group',
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
            'body': json.dumps({'message': str(e),'ff':body})
        }