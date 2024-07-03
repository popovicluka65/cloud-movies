import json
import uuid

import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable'
from boto3.dynamodb.conditions import Key,Attr


def search_lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }
    table = dynamodb.Table(table_name)

    # Pretraga u globalnom sekundarnom indeksu
    try:

        search_params = json.loads(event['body'])

        title = search_params.get('title')
        description = search_params.get('description')
        director = search_params.get('director')
        actors = search_params.get('actors')
        genre = search_params.get('genres')

        # Kreiranje filter izraza na osnovu parametara
        filter_expression = []
        expression_attribute_values = {}

        if title!="":
            filter_expression.append('title = :title')
            expression_attribute_values[':title'] = title

        if actors!="":
            filter_expression.append('actors = :actors')
            expression_attribute_values[':actors'] = actors
            actors_list = actors.split(',')

        director_list=[]
        if director!="":
            filter_expression.append('director = :director')
            expression_attribute_values[':director'] = director
            director_list = director.split(',')

        if description!="":
            filter_expression.append('description = :description')
            expression_attribute_values[':description'] = description

        # if not isinstance(genre, list):
        #     if genre!="":
        #         filter_expression.append('genres = :genres')
        #         expression_attribute_values[':genres'] = genre
        # else:
        #         # Ako je žanr lista, tretirajte kao da tražite bilo koji od žanrova
        #         genre_filters = []
        #         for g in genre:
        #             genre_filters.append('contains(genres, :genre)')
        #             expression_attribute_values[':genre'] = g
        #         filter_expression.append(' OR '.join(genre_filters))

        #filter_expression = ' AND '.join(filter_expression)

        search_query = generate_all_attributes(search_params)
        all_q=generate_all_q(search_params)

        # params = {
        #     'FilterExpression': 'username IN (:user1, :user2)',
        #     'ExpressionAttributeValues': {
        #         ':user1': 'john',
        #         ':user2': 'mike'
        #     }
        # }

        # filter_expression = None
        #
        # for direct in director_list:
        #     if filter_expression is None:
        #         filter_expression = Attr('director').contains(direct)
        #     else:
        #         filter_expression = filter_expression | Attr('director').contains(direct)

        # filter_expression = ""
        #
        # for direct in director_list:
        #     if filter_expression:
        #         filter_expression += " OR "
        #     filter_expression += f"contains(all_attributes, :direct_{direct.replace(' ', '_')})"
        #     expression_attribute_values[f":direct_{direct.replace(' ', '_')}"] = direct


        response = table.query(
                IndexName='AllAttributesIndex10',
                KeyConditionExpression=Key('all_attributes').eq(search_query),
        )

        return {
            'headers':headers,
            'statusCode': 200,
            'body':json.dumps({'SQ':str(search_query), 'RES':str(Key('all_attributes')), 'EXPRESION':expression_attribute_values, 'COUNT':response['Items']})
        }
    except Exception as e:
        print(e)
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def generate_all_attributes(params):
    genres = params.get('genres')
    genres_str = ','.join(genres) if isinstance(genres, list) else ''
    return f"{params.get('title', '')}_{params.get('actors', '')}_{params.get('director', '')}_{params.get('description', '')}_[{genres_str}]"

def generate_all_q(params):
    title = params.get('title')
    description = params.get('description')
    director = params.get('director')
    actors = params.get('actors')
    genre = params.get('genres')

    actors_list = []
    if actors != "":
        actors_list = params.get('actors').split(',')

    director_list = []
    if director != "":
        director_list = params.get('director').split(',')

    queues=[]

    for act in actors_list:
        a=act.strip()
        for dir in director_list:
            d=dir.strip()
            s=f"{params.get('title', '')}_{a}_{d}_{params.get('description', '')}"
            queues.append(s)

    #q=generate_all_attributes(params)
    #queues.append(q)
    return queues
