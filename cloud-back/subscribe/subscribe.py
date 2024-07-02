import json
import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
table_name = 'Subscription100Table'  # Ime DynamoDB tabele
sns_client = boto3.client('sns')


def lambda_handler(event, context):
    topic_arn = 'arn:aws:sns:eu-central-1:992382767224:MovieTopic'
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
        subscriber = body['subscriber']
        query = body['query']
        content_creator = body['content']

        generated_uuid = str(uuid.uuid4())
        subscription_id = generated_uuid  # Ispravljena promenljiva
        item = {
            'subscription_id': subscription_id,
            'subscriber': subscriber,
            'type': query,
            'content_creator': content_creator
        }

        table.put_item(Item=item)

        # Pretplata korisnika na SNS topic
        sns_subscription_response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',  # Ili 'sms' ili neki drugi protokol koji koristite
            Endpoint="popovicluka65@gmail.com",  # Email adresa ili broj telefona pretplatnika
            # Attributes={
            #     'FilterPolicy': json.dumps({
            #         'query': [query]
            #     })
            # }

        )

        # Slanje obaveštenja putem SNS-a
        message = f"Novi sadržaj je objavljen od strane {content_creator}. Pretplatnik: {subscriber}, Tip: {query}"
        # sns_response = sns_client.publish(
        #     TopicArn=topic_arn,
        #     Message=message,
        #     Subject='Obaveštenje o novom sadržaju'
        # )

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
