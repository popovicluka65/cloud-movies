import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
table_name = 'Subscription2Table'  # Ime DynamoDB tabele

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

        generated_uuid = str(uuid.uuid4())
        #posle obrisati samo proveriti da li se unosi id
        subsribtion_id = generated_uuid
        item = {
            'subscription_id':subsribtion_id,
            'subscriber': "popovicluka65@gmail.com", #subscriber
            'content': "NEKI GLUMAC"
        }

        table.put_item(Item=item)

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