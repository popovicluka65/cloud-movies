import json
import uuid

import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name_feed = 'Feed100Table'
table_name='MoviesTable100'

def get_feed_handler(event, context):
    table_feed = dynamodb.Table(table_name_feed)
    table=dynamodb.Table(table_name)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    try:
        #body = json.loads(event['body'])
        #user_id = body['user_id']
        path = event['path']
        path_parts = path.split('/')
        user_id = path_parts[-1]
        response = table_feed.get_item(Key={'user_id': user_id})
        movies_list = response['Item']['movies_ids']

        response = table.scan()

        all_movies = response['Items']

        print(movies_list)

        print(all_movies)

        return_movies=[]

        for my_movie in movies_list:
            for movie in all_movies:
                movie_id_all=movie['movie_id']
                if my_movie==movie_id_all:
                    return_movies.append(movie)


        return {
            'headers':headers,
            'statusCode': 200,
            'body': json.dumps(return_movies)
        }
    except Exception as e:
        print(e)
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }