import urllib.parse

import boto3
import json

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable'  # Ime DynamoDB tabele


def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'

    }
    old_key = event['pathParameters']['id']
    split = old_key.split(":")
    movie_id = split[0]
    title = split[1]
    decoded_key = urllib.parse.unquote(title)
    # movie_id = urllib.parse.unquote(old_key)
    try:
        if not old_key:
            raise ValueError('ID parameter is required.')


        response = table.get_item(
            Key={
                'movie_id': movie_id,
                'title': decoded_key
            }
        )

        # Provera da li je stavka pronađena
        if 'Item' not in response:
            raise ValueError(f'Movie with ID {old_key} not found.')

        movie = response['Item']

        return {
            'headers': headers,
            'statusCode': 200,
            'body': json.dumps(movie)
        }
    except Exception as e:
        print(e)
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }