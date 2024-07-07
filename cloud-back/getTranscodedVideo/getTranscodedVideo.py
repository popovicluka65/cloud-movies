import json
import boto3
import os
import urllib.parse

s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'
def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    try:
        print("Received event:", json.dumps(event))
        body = json.loads(event['body'])
        movie_id = body['movie_id']

        url = s3.generate_presigned_url('get_object',
                                                 Params={'Bucket': S3_BUCKET_NAME, 'Key':"movies/"+movie_id },
                                                 ExpiresIn=3600)
        return {
                 'statusCode': 200,
                 "headers": headers,
                'body': json.dumps({
                'message': movie_id,
                'response':url
                })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error generating URL: {str(e)}'
        }
