import json
import uuid
import boto3
import os

from botocore.exceptions import PartialCredentialsError, NoCredentialsError

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable'

def upload_dynamo_handler(event, context):

        try:
            print("Received event:", json.dumps(event))

            # Uzimamo podatke direktno iz event objekta
            body = event

            print("Parsed body:", body)  # Debug

            title = body.get('title', '')
            description = body.get('description', '')
            actors = body.get('actors', '')
            director = body.get('director', '')
            genres = body.get('genres', '')
            name = body.get('name', '')
            type = body.get('type', '')
            size = body.get('size', '')
            date_created = body.get('dateCreated', '')  # Note: Use the same key as in input_data
            date_modified = body.get('dateModified', '')  # Note: Use the same key as in input_data

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

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Item inserted successfully'})
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({f'f:message: ': str(e)})
            }
