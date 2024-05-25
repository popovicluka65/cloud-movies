import json
import boto3


dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable'  # Ime vaše DynamoDB tabele


def lambda_handler(event, context):
    print("UDJE U LAMBDU")
    table = dynamodb.Table(table_name)
    try:
        # Querying the table
        response = table.scan()  # Ovo će vratiti sve stavke iz tabele, može se prilagoditi za specifične query-je

        # Formiranje odgovora
        movies = response['Items']
        return {
            'statusCode': 200,
            'body': json.dumps(movies)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }