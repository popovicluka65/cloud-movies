import json
import uuid

import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable'
from boto3.dynamodb.conditions import Key


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
        director = search_params.get('directors')
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

        # if director!="":
        #     filter_expression.append('director = :director')
        #     expression_attribute_values[':director'] = director

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

        # # Spajanje filter izraza
        filter_expression = ' AND '.join(filter_expression)

        search_query=generate_all_attributes(search_params)


        response = table.query(
            IndexName='AllAttributesIndex',  # Ime globalnog sekundarnog indeksa
            KeyConditionExpression=Key('all_attributes').eq(search_query),
            FilterExpression=filter_expression if filter_expression else None,
            ExpressionAttributeValues=expression_attribute_values if expression_attribute_values else None
        )

        return {
            'headers':headers,
            'statusCode': 200,
            'body':filter_expression
        }
    except Exception as e:
        print(e)
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def generate_all_attributes(params):
    return f"{params.get('title', '')}_{params.get('description', '')}_{params.get('actors', '')}"
   #return f"{params.get('title', '')}_{params.get('description', '')}_{params.get('actors', '')}_{params.get('genres', '')}"
