import json
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'Review100Table'
def add_review_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    try:
        print("Received event:", json.dumps(event))
        body = json.loads(event['body'])
        user_id = body['username']
        rate = body['rate']
        movie_id = body['movie_id']
        title = body['title']

        table = dynamodb.Table(table_name)

        generated_uuid = str(uuid.uuid4())

        item = {
            'review_id': generated_uuid,
            'user_id': user_id,
            'rate': rate,
            'movie_id':movie_id,
            'title':title
        }

        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Review added successfully', 'review_id': generated_uuid}),
            'headers': headers
        }

    except NoCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Credentials not available'}),
            'headers': headers
        }
    except PartialCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Incomplete credentials provided'}),
            'headers': headers
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)}),
            'headers': headers
        }