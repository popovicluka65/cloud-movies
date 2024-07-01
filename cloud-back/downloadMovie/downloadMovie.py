import json
import boto3
import os
import urllib.parse


s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'
table_name = 'MoviesTable'

def download_movie_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    key = event['pathParameters']['id']
    decoded_key = urllib.parse.unquote(key)

    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=decoded_key)

        if 'Contents' in response and any(obj['Key'] == decoded_key for obj in response['Contents']):
            url = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': S3_BUCKET_NAME, 'Key': decoded_key},
                                            ExpiresIn=3600)
            return {
                'headers': headers,
                'statusCode': 200,
                'body': url
            }
        else:
            return {
                'headers': headers,
                'statusCode': 404,
                'body': 'Object not found: ' + decoded_key
            }
    except Exception as e:
        return {
            'headers': headers,
            'statusCode': 500,
            'body': f'Error generating URL: {str(e)}'
        }

