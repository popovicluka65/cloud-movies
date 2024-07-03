import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
table_name = 'Subscription100Table'  # Ime DynamoDB tabele
sns_client = boto3.client('sns')
topic_arn = 'arn:aws:sns:eu-central-1:992382767224:MovieTopic'
table = dynamodb.Table(table_name)
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
}

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        body = json.loads(event['body'])
        subscriber = body['subscriber']
        subscriber_email = body['email']
        query = body['query']
        content_creator = body['content']

        generated_uuid = str(uuid.uuid4())
        subscription_id = generated_uuid  # Ispravljena promenljiva
        item = {
            'subscription_id': subscription_id,
            'subscriber': subscriber,
            'subscriber_email':subscriber_email,
            'type': query,
            'content_creator': content_creator
        }

        table.put_item(Item=item)

        sns_subscription_response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',  # Ili 'sms' ili neki drugi protokol koji koristite
            Endpoint=subscriber_email,  # Email adresa ili broj telefona pretplatnika
        )

        # Slanje obaveštenja putem SNS-a
        message = f"Novi sadržaj je objavljen od strane {content_creator}. Pretplatnik: {subscriber}, Tip: {query}"
        sns_response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='Obaveštenje o novom sadržaju'
        )

        return {
            'headers': headers,
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successful subscription and notification sent',
                'subscription_id': subscription_id,
                'sns_message_id': sns_response['MessageId'],
                'sns_subscription_arn': sns_subscription_response['SubscriptionArn']
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


def get_subscribes(event, context):
    try:
        print("Received event:", json.dumps(event))
        body = json.loads(event['body'])
        username = body['username']
        response = table.scan()

        items = response['Items']
        for item in items:
            print(item)

        body_response = {
            'message': 'Successful get subscribe',
            'items': items # Dodajte stavke iz DynamoDB tabele u odgovor
        }

        # Vraćanje HTTP odgovora
        return {
            'headers': headers,
            'statusCode': 200,
            'body': json.dumps(body_response)
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
