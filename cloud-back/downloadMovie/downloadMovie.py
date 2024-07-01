import json
import boto3
import os
import urllib.parse


s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'
table_name = 'MoviesTable'

def download_movie_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    # HERE FIRST FROM MOVIETABLE LOAD

    # Dodavanje GSI u postojeću tabelu
    response = dynamodb.update_table(
        TableName='MoviesTable',
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        GlobalSecondaryIndexUpdates=[
            {
                'Create': {
                    'IndexName': 'TitleIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'title',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            }
        ]
    )

    # Referenciranje tabele
    table = dynamodb.Table('MoviesTable')



    # Provera da li su pronađeni filmovi
    if 'Items' in response:
        items = response['Items']
        for item in items:
            print(item)
    else:
        print("Nema filmova sa datim naslovom.")

    try:
        key = event['pathParameters']['id']
        decoded_key = urllib.parse.unquote(key)
    except KeyError:
        return {
            'statusCode': 400,
            'body': 'Invalid input, "movieId" is required in path parameters',
            'headers': headers
        }

    object_key = f"movies/{decoded_key}"

    try:
        # Pretraživanje tabele koristeći GSI
        response = table.query(
            IndexName='TitleIndex',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('title').eq(object_key)
        )
        return {
            'headers': headers,
            'statusCode': 200,
            'body': response
        }
    except Exception as e:
        return {
                'headers': headers,
                'statusCode': 500,
                'body': f'Error generating URL: {str(e)}'
            }





    # s3 = boto3.client('s3')
    #
    # try:
    #     response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=object_key)
    #
    #     if 'Contents' in response and any(obj['Key'] == object_key for obj in response['Contents']):
    #         url = s3.generate_presigned_url('get_object',
    #                                         Params={'Bucket': S3_BUCKET_NAME, 'Key': object_key},
    #                                         ExpiresIn=3600)
    #         return {
    #             'headers': headers,
    #             'statusCode': 200,
    #             'body': url
    #         }
    #     else:
    #         return {
    #             'headers': headers,
    #             'statusCode': 404,
    #             'body': 'Object not found: ' + object_key
    #         }
    # except Exception as e:
    #     return {
    #         'headers': headers,
    #         'statusCode': 500,
    #         'body': f'Error generating URL: {str(e)}'
    #     }

