import json
import uuid

import boto3
import os
import urllib.parse
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable'
s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'

def upload_data_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    try:
        print("Received event:", json.dumps(event))
        body = json.loads(event['body'])
        title = body['title']
        description = body['description']
        actors = body['actors']
        director = body['director']
        genres = body['genres']
        name = body['name']
        type = body['type']
        size = str(body['size'])
        date_created = body['dateCreated']
        date_modified = body['dateModified']

        table = dynamodb.Table(table_name)

        generated_uuid = str(uuid.uuid4())

        item = {
            'movie_id':generated_uuid,
            'title': title,
            'description': description,
            'actors': actors,
            'director': director,
            'genres': genres,
            'name': name,
            'type': str(type),
            'size': str(size),
            'date_created': str(date_created),
            'date_modified': str(date_modified)
        }

        table.put_item(Item=item)

        try:
            s3.head_bucket(Bucket=S3_BUCKET_NAME)
            presigned_url = s3.generate_presigned_url(
                'put_object',
                Params={'Bucket': S3_BUCKET_NAME, 'Key': f"{S3_FOLDER_PATH}{generated_uuid}"},
                ExpiresIn=3600
            )

            print(presigned_url)
        except Exception as e:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': str(e)}),
                'headers': headers
            }
        return {
            'statusCode': 200,
            'headers': headers,
            'body': presigned_url
        }
    except NoCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Credentials not available'}),
            'headers': headers
        }
    except PartialCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Incomplete credentials provided'}),
            'headers': headers
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(body)}),
            'headers': headers
        }