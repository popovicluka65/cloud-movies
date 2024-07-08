import boto3
import json

sqs_arn = "https://sqs.eu-central-1.amazonaws.com/992382767224/CloudBackStack-UploadSQS4BB1896E-T93YQkfluhSC"
sqs = boto3.client('sqs')
S3_FOLDER_PATH = 'movies/'
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
# S3_FOLDER_PATH = 'movies/'
s3 = boto3.client('s3')


def send_transcode_message_handler(event, context):
    # resolutions = [360, 480, 720]
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    try:
        body = json.loads(event['body'])
        generated_uuid = body['id']
        s3.head_object(Bucket=S3_BUCKET_NAME, Key=S3_FOLDER_PATH + generated_uuid)
        resolutions = []
        width_height = {
            360: [640, 360],
            480: [854, 480],
            720: [1280, 720]
        }
        resolutions.append(width_height[360])
        resolutions.append(width_height[480])
        resolutions.append(width_height[720])

        list_of_shared_data = []
        for resolution in resolutions:
            shared_data = {
                "movie_id": generated_uuid,
                "resolution": resolution,
                "S3_FOLDER_PATH": S3_FOLDER_PATH
            }

            list_of_shared_data.append(shared_data)

        sqs.send_message(
            QueueUrl=sqs_arn,
            MessageBody=json.dumps({'sharedData': list_of_shared_data})
        )

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(generated_uuid)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(e)
        }
