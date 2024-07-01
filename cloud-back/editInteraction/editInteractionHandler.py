import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable'
table_interacion='Interaction100Table'
table_feed='Feed100Table'
table_review='Review100Table'
table_sub='Subscription100Table'
table_download='Download100Table'


def lambda_handler(event, context):         #AKO BUDE SPORO, NAPRAVITI 2 FUNKCIJE, JEDNU IZMENA, DRUGA CREATE
    table = dynamodb.Table(table_name)
    table_subs=dynamodb.Table(table_sub)
    table_downloads=dynamodb.Table(table_download)
    table_reviews=dynamodb.Table(table_review)
    table_interacions=dynamodb.Table(table_interacion)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    try:
        body = json.loads(event['body'])
        user_id = body['username']

        #Ovde sad treba kreirati tabelu sa User1, vrednosti u paru (comedy, 5) ...

        values_subscription=table_subs.query(
            IndexName='subscriber-index',
            KeyConditionExpression='subscriber = :subscriber',
            ExpressionAttributeValues={
                ':subscriber': user_id
            }
        )

        # values_review = table_review.query(
        #       IndexName='user_id',
        #       KeyConditionExpression=Key('user_id').eq(user_id)
        #   )
        #
        #
        # values_download = table_download.query(
        #     KeyConditionExpression=Key('user_id').eq(user_id)
        # )


        # if not values_subscription['Items'] and not values_review['Items'] and not values_download['Items']:
        #     pass #vratiti get movies kao sortirani po datumima

        dict={}
        #
        # for item in values_subscription['Items']:           #ovo je jacine 5 (subscribe)
        #     content = item.get('content')
        #     if content in dict.keys():
        #         dict[content]+=5
        #     else:
        #         dict[content]=5
        #
        # # for item in values_review['Items']:
        # #     content=item.get('rate')
        #
        # for item in values_download['Items']:
        #     actors=item.get('actors')
        #     directors=item.get('director')
        #     genres=item.get('genres')
        #     for actor in actors:
        #         if actor in dict.keys():
        #             dict[actor]+=2
        #         else:
        #             dict[actor]=2
        #     for director in directors:
        #         if director in dict.keys():
        #             dict[director]+=2
        #         else:
        #             dict[director]=2
        #     for genre in genres:
        #         if genre in dict.keys():
        #             dict[genre]+=2
        #         else:
        #             dict[genre]=2



        list=[]             #ubacujemo u listu sve vrednosti, i posle ih sortiramo ('ime filma + vrednost) (tuple da bude)

        #sortirati listu

        #namestiti u tabeli

        return {
            'headers': headers,
            'statusCode': 200,
            'body': json.dumps(user_id)
        }
    except Exception as e:
        print(e)
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'error': str(user_id)})
        }