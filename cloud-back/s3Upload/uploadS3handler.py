import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import uuid

s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'
def upload_S3_handler(event, context):
    generated_uuid = str(uuid.uuid4())
    try:
        s3.head_bucket(Bucket=S3_BUCKET_NAME)
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': f"{S3_FOLDER_PATH}{generated_uuid}"},
            ExpiresIn=3600
        )

        print(presigned_url)
    except Exception as e:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': str(e)})
        }

    except NoCredentialsError:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Credentials not available'})
            }
    except PartialCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Incomplete credentials provided'})
        }
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'message': 'Movie added successfully!',
            'upload_url': presigned_url
        })
    }
