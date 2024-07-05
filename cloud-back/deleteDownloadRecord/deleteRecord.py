import boto3


def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Download100Table'

    table = dynamodb.Table(table_name)

    movie_id = event.get('movie_id')

    try:
        response = table.query(
            IndexName='movie_id-index',  # Ime globalnog sekundarnog indeksa
            KeyConditionExpression=dynamodb.conditions.Key('movie_id').eq(movie_id)
        )

        with table.batch_writer() as batch:
            for item in response['Items']:
                batch.delete_item(Key={'download_id': item['download_id']})

        return {
            'statusCode': 200,
            'body': 'Stavke su uspešno obrisane.',
            'headers': headers
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Greška pri brisanju stavki: {str(e)}',
            'headers': headers
        }