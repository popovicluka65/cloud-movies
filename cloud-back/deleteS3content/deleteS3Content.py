import boto3
import json
s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'

def delete_s3content_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    try:
        movie_id = event['movie_id']

        s3.delete_object(Bucket=S3_BUCKET_NAME, Key=f"{S3_FOLDER_PATH}{movie_id}")

        return {
            'statusCode': 200,
            'body': f"Deleted object with key {movie_id} from bucket {S3_BUCKET_NAME}.",
            'headers': headers
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(event['body'])}),
            'headers': headers
        }