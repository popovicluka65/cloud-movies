import json
import boto3
import os

s3 = boto3.client('s3')

def download_movie_handler(event, context):
    bucket_name = os.environ['content-bucket-cloud-app-movie2']
    key = event['queryStringParameters']['key']

    try:
        url = s3.generate_persigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key},ExpiresIn=3600)
        return {
            'statusCode': 200,
            'body': json.dumps({'url':url})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }