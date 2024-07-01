import json
import uuid

import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = 'Feed10Table'

def get_feed_handler(event, context):
    table = dynamodb.Table(table_name)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        response = table.get_item(Key={'user_id': user_id})
        movies = response['Items']

        return {
            'headers':headers,
            'statusCode': 200,
            'body': json.dumps(movies)
        }
    except Exception as e:
        print(e)
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }