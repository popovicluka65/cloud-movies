import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from boto3.dynamodb.conditions import Key  # Dodaj ovaj import

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable100'
s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,DELETE',
    'Access-Control-Allow-Headers': 'Content-Type'
}
def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    try:
        path = event['path']
        path_parts = path.split('/')
        partition_key_value = path_parts[-1]
        print(partition_key_value)

        responseDynamo = table.delete_item(
            Key={
                'movie_id': partition_key_value
            }
        )

        responseS3 = s3.delete_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"{S3_FOLDER_PATH}{partition_key_value}"
        )

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