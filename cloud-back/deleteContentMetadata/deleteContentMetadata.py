import boto3
import json


def delete_metadata_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name = 'MoviesTable100'
        movie_id = event['movie_id']

        table = dynamodb.Table(table_name)

        table.delete_item(
            Key={
                'movie_id': movie_id
            }
        )

        return {
            'statusCode': 200,
            'body': f"Deleted item with movie_id {movie_id} from table {table_name}.",
            'headers': headers
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(event['body'])}),
            'headers': headers
        }