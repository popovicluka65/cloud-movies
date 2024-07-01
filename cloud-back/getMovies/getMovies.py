import decimal
import json
import boto3


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
    try:
        # Querying the table
        response = table.scan()

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