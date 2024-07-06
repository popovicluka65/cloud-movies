import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable100'
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
    table_feeds=dynamodb.Table(table_feed)
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
            IndexName='subscriber-index4',
            KeyConditionExpression='subscriber_email = :subscriber_email',
            ExpressionAttributeValues={
                ':subscriber_email': user_id
            }
        )

        responseReview = table_reviews.scan()
        itemsReview = responseReview['Items']
        while 'LastEvaluatedKey' in responseReview:
            response = table_review.scan(ExclusiveStartKey=responseReview['LastEvaluatedKey'])
            itemsReview.extend(response['Items'])
        # values_review = table_reviews.query(
        #     KeyConditionExpression='user_id = :user_id',
        #     ExpressionAttributeValues={
        #         ':user_id': user_id
        #     }
        # )
        # values_review = table_review.query(
        #     IndexName='review-index-dynamo',
        #     key_condition_expression=Key('user_id').eq(user_id) & Key('rate').eq(rate)
        # )
        #
        #
        # values_download = table_download.query(
        #     KeyConditionExpression=Key('user_id').eq(user_id)
        # )

        responseDownload = table_downloads.scan()
        itemsDownloads = responseDownload['Items']
        while 'LastEvaluatedKey' in responseDownload:
            response = table_downloads.scan(ExclusiveStartKey=responseDownload['LastEvaluatedKey'])
            itemsDownloads.extend(response['Items'])

        responseMovies = table.scan()
        itemsMovies = responseMovies['Items']
        while 'LastEvaluatedKey' in responseMovies:
            response = table.scan(ExclusiveStartKey=responseMovies['LastEvaluatedKey'])
            itemsMovies.extend(response['Items'])

        dict={}
        #
        for item in values_subscription['Items']:           #ovo je jacine 5 (subscribe)
            content = item.get('type')
            if content in dict.keys():
                a=str(content)
                dict[a]+=5
            else:
                a=str(content)
                dict[a]=5

        points_download=3
        for downloadItem in itemsDownloads:                 #ovo je jacine 3 (download)
            id_download=downloadItem.get('movie_id')
            user=downloadItem.get('user_id')
            if user_id==user:
                for movie in itemsMovies:
                    id_movie=movie.get('movie_id')
                    actors=movie.get('actors')
                    directors=movie.get('director')
                    genres_list=movie.get('genres')
                    if id_download==id_movie:
                        actor_list = actors.split(',')
                        directors_list = directors.split(',')
                        for actor in actor_list:
                            act=actor.strip()
                            if act in dict.keys():
                                dict[act]+=points_download
                            else:
                                dict[act]=points_download
                        for director in directors_list:
                            dir=director.strip()
                            if dir in dict.keys():
                                dict[dir]+=points_download
                            else:
                                dict[dir]=points_download
                        for genre_item in genres_list:
                            gen=genre_item
                            if gen in dict.keys():
                                dict[gen]+=points_download
                            else:
                                dict[gen]=points_download

        for reviewItem in itemsReview:
            id_review = reviewItem.get('movie_id')
            rate_review=reviewItem.get('rate')
            user = reviewItem.get('user_id')
            if user_id==user:
                for movie in itemsMovies:
                    id_movie=movie.get('movie_id')
                    actors=movie.get('actors')
                    directors=movie.get('director')
                    genres_list=movie.get('genres')
                    if id_review==id_movie:
                        actor_list = actors.split(',')
                        directors_list = directors.split(',')
                        for actor in actor_list:
                            act=actor.strip()
                            if act in dict.keys():
                                dict[act]+=int(rate_review)-3                #5 ->2 ... 1 ->-2
                            else:
                                dict[act]=int(rate_review)-3
                        for director in directors_list:
                            dir=director.strip()
                            if dir in dict.keys():
                                dict[dir]+=int(rate_review)-3
                            else:
                                dict[dir]=int(rate_review)-3
                        for genre_item in genres_list:
                            gen=genre_item
                            if gen in dict.keys():
                                dict[gen]+=int(rate_review)-3
                            else:
                                dict[gen]=int(rate_review)-3

        movies_values={}

        movies_values1={}

        p=3

        for movie in itemsMovies:
            value_movie=0
            id_movie = movie.get('movie_id')
            actors = movie.get('actors')
            directors = movie.get('director')
            genres_list=movie.get('genres')
            actors_list=actors.split(",")
            directors_list=directors.split(",")
            date_created = movie.get('date_created')
            for key, value in dict.items():
                for actor in actors_list:
                    ac=actor.strip()
                    if ac==key:
                        value_movie+=value
                for director in directors_list:
                    dir=director.strip()
                    if dir==key:
                        value_movie+=value
                for genre in genres_list:
                     gen = genre
                     if gen==key:
                         value_movie+=value
            given_date = datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            today = datetime.utcnow().date()
            three_days_ago = today - timedelta(days=3)
            seven_days_ago = today - timedelta(days=7)
            if given_date==today:
                p=5
                value_movie*=3
            if three_days_ago<=given_date<today:
                value_movie *= 2
            if seven_days_ago<=given_date<three_days_ago:
                value_movie*=1.3
            movies_values[id_movie] = (value_movie,given_date)
           # movies_values[id_movie]=value_movie

        today_iso_format = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        #sorted_movies_values = {k: v for k, v in sorted(movies_values.items(), key=lambda item: item[1], reverse=True)}

        #sorted_movies_values = {k: v for k, v in sorted(movies_values.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)}

        sorted_movies_values = {k: v for k, v in sorted(movies_values.items(), key=lambda item: (item[1][0], -abs(today - item[1][1])), reverse=True)}

        print(sorted_movies_values)

        interaction_movies_values={}

        feed_movies_values = []

        for key, value in sorted_movies_values.items():
            a,b=value
            date_str = b.strftime('%Y-%m-%d')
            print(date_str)
            interaction_movies_values[key]=(a,date_str)

        print(interaction_movies_values)

        item = {
            'user_id': user_id,
            'values': json.dumps(interaction_movies_values)
        }

        table_interacions.put_item(Item=item)

        for key, value in interaction_movies_values.items():
            feed_movies_values.append(key)

        item1 = {
            'user_id': user_id,
            'movies_ids': feed_movies_values
        }

        table_feeds.put_item(Item=item1)

        # item = {
        #     'user_id': {'S': user_id},
        #     'content': {'M': dict}
        # }

        # try:
        #     response = dynamodb_client.put_item(
        #         TableName=table_interacion,
        #         Item=item
        #     )
        #     print("Stavka uspešno dodata:", response)
        # except Exception as e:
        #     print("Greška pri dodavanju stavke:", e)

        list=[]             #ubacujemo u listu sve vrednosti, i posle ih sortiramo ('ime filma + vrednost) (tuple da bude)

        #sortirati listu

        #namestiti u tabeli

        return {
            'headers': headers,
            'statusCode': 200,
            'body': json.dumps({"DICT":dict, "A":values_subscription, "RE":str(p)})
        }
    except Exception as e:
        print(e)
        return {
            'headers': headers,
            'statusCode': 500,
            'body': json.dumps({'error': json.dumps(e)})
        }