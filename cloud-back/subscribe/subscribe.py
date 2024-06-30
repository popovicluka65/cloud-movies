import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
table_name = 'SubscriptionTable'  # Ime DynamoDB tabele
s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    try:
        print("Received event:", json.dumps(event))
        body = json.loads(event['body'])
        # title = body['title']
        # description = body['description']


        #table = dynamodb.Table(table_name)

        generated_uuid = str(uuid.uuid4())
        #posle obrisati samo proveriti da li se unosi id
        subsribtion_id = generated_uuid
        item = {
            'subscription_id':subsribtion_id,
            'subscriber': "popovicluka65@gmail.com", #subscriber
            'content': "NEKI GLUMAC"
        }

        table.put_item(Item=item)

        try:
            s3.head_bucket(Bucket=S3_BUCKET_NAME)
            # presigned_url = s3.generate_presigned_url(
            #     'put_object',
            #     Params={'Bucket': S3_BUCKET_NAME, 'Key': f"{S3_FOLDER_PATH}{subsribtion_id}"},
            #     ExpiresIn=3600
            # )

            #print(presigned_url)
        except Exception as e:
            return {
                'headers': headers,
                'statusCode': 404,
                'body': json.dumps({'message': str(e)})
            }
        return {
            'headers': headers,
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successful subscription',
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