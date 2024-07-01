import boto3
import json
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = 'Download10Table'


def download_record_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    print("Received event:", json.dumps(event))
    body = json.loads(event['body'])

    try:

        print("Parsed body:", body)  # Debug

        user_id = body['userId']
        movie_id = body['movie_id']
        title = body['title']

        table = dynamodb.Table(table_name)
        generated_uuid = str(uuid.uuid4())

        item = {
            'download_id': generated_uuid,
            'user_id': user_id,
            'movie_id': movie_id,
            'title': title,
        }

        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item inserted successfully'}),
            'headers': headers
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({f'f:message: ': str(e)}),
            'headers': headers
        }
