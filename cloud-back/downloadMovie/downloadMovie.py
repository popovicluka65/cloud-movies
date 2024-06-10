import json
import boto3
import os
import urllib.parse


s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'

def download_movie_handler(event, context):

    try:
        key = event['pathParameters']['id']
        decoded_key = urllib.parse.unquote(key)
    except KeyError:
        return {
            'statusCode': 400,
            'body': 'Invalid input, "movieId" is required in path parameters'
        }

    object_key = f"movies/{decoded_key}"

    s3 = boto3.client('s3')

    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=object_key)

        if 'Contents' in response and any(obj['Key'] == object_key for obj in response['Contents']):
            url = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': S3_BUCKET_NAME, 'Key': object_key},
                                            ExpiresIn=3600)
            return {
                'statusCode': 200,
                'body': url
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Object not found: ' + object_key
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error generating URL: {str(e)}'
        }

