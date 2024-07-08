import json
import uuid

import boto3
import os
import urllib.parse
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table_name = 'MoviesTable100'
s3 = boto3.client('s3')
S3_BUCKET_NAME = 'content-bucket-cloud-app-movie2'
S3_FOLDER_PATH = 'movies/'

sns = boto3.client('sns')
sns_topic_arn = 'arn:aws:sns:eu-central-1:992382767224:MovieTopic'
sns_topic_arn_email = 'arn:aws:sns:eu-central-1:992382767224:MovieTopic/email/'
subscribe_table_name = 'Subscription100Table'
table_interacion='Interaction100Table'
table_feed='Feed100Table'
table_review='Review100Table'
table_download='Download100Table'
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
        table_interacions = dynamodb.Table(table_interacion)
        table_feeds = dynamodb.Table(table_feed)

        generated_uuid = ""
        if 'id' in body:
            generated_uuid = body['id']
        else:
            generated_uuid = str(uuid.uuid4())

        all_attributes=title+"_"+actors+"_"+director+"_"+description+"_["

        genres_str = ','.join(genres) if isinstance(genres, list) else ''

        all_attributes=all_attributes+genres_str+"]"


        item = {
            'movie_id': generated_uuid,
            'title': title,
            'description': description,
            'actors': actors,
            'director': director,
            'genres': genres,
            'name': name,
            'type': str(type),
            'size': str(size),
            'date_created': str(date_created),
            'date_modified': str(date_modified),
            'all_attributes':all_attributes
        }

        table.put_item(Item=item)

        # Slanje notifikacije na SNS temu
        send_notifications(title,director,actors,genres)

        responseFeed = table_feeds.scan()
        itemsFeed = responseFeed['Items']
        while 'LastEvaluatedKey' in responseFeed:
            response = table_feeds.scan(ExclusiveStartKey=responseFeed['LastEvaluatedKey'])
            itemsFeed.extend(response['Items'])

        print(itemsFeed)

        for item in itemsFeed:
            user_id = item['user_id']
            edit_feed_table(user_id)

        try:
            s3.head_bucket(Bucket=S3_BUCKET_NAME)
            presigned_url = s3.generate_presigned_url(
                'put_object',
                Params={'Bucket': S3_BUCKET_NAME, 'Key': f"{S3_FOLDER_PATH}{generated_uuid}"},
                ExpiresIn=3600
            )

            response_body = {
                'presigned_url': presigned_url,
                'uuid': generated_uuid
            }

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
            'body': json.dumps(response_body)

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

def send_notifications(title,director,actors,genres):
    subscriptions = dynamodb.Table(subscribe_table_name)
    response = subscriptions.scan()
    items = response.get('Items', [])
    print(items)
    emails = []
    print("ITEMS")
    for item in items:
        print(item)
        if item['type'] == director:
            emails.append(item['subscriber_email'])
        if item['type'] in actors:
            emails.append(item['subscriber_email'])
        if item['type'] in genres:
            emails.append(item['subscriber_email'])

    try:
        message = f"Novi film " + title + " je dostupan! Pogledajte ga sada.\n"
        message = f"Reziser " +  director+  ", glumci : "+actors+", zanrovi"+genres+".\n"

        response = sns.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='Novi film dostupan'
        )
    except Exception as e:
        print("Error publishing SNS message:", str(e))


def edit_feed_table(username):
    try:
        table = dynamodb.Table(table_name)
        table_subs = dynamodb.Table(subscribe_table_name)
        table_downloads = dynamodb.Table(table_download)
        table_reviews = dynamodb.Table(table_review)
        table_interacions = dynamodb.Table(table_interacion)
        table_feeds = dynamodb.Table(table_feed)

        print("UDJE OVDEEEEEEE")
        user_id = username

        # Ovde sad treba kreirati tabelu sa User1, vrednosti u paru (comedy, 5) ...

        values_subscription = table_subs.query(
            IndexName='subscriber-index4',
            KeyConditionExpression='subscriber_email = :subscriber_email',
            ExpressionAttributeValues={
                ':subscriber_email': user_id
            }
        )

        responseReview = table_reviews.scan()
        itemsReview = responseReview['Items']
        while 'LastEvaluatedKey' in responseReview:
            responseReview = table_reviews.scan(ExclusiveStartKey=responseReview['LastEvaluatedKey'])
            itemsReview.extend(responseReview['Items'])

        responseDownload = table_downloads.scan()
        itemsDownloads = responseDownload['Items']
        print("OVDE1")
        while 'LastEvaluatedKey' in responseDownload:
            responseDownload = table_downloads.scan(ExclusiveStartKey=responseDownload['LastEvaluatedKey'])
            itemsDownloads.extend(responseDownload['Items'])

        responseMovies = table.scan()
        itemsMovies = responseMovies['Items']
        print("OVDE2")
        while 'LastEvaluatedKey' in responseMovies:
            responseMovies = table.scan(ExclusiveStartKey=responseMovies['LastEvaluatedKey'])
            itemsMovies.extend(responseMovies['Items'])

        print("OVDE3")
        dict = {}

        for item in values_subscription['Items']:  # ovo je jacine 5 (subscribe)
            content = item.get('type')
            if content in dict.keys():
                a = str(content)
                dict[a] += 5
            else:
                a = str(content)
                dict[a] = 5

        points_download = 3
        for downloadItem in itemsDownloads:  # ovo je jacine 3 (download)
            id_download = downloadItem.get('movie_id')
            user = downloadItem.get('user_id')
            if user_id == user:
                for movie in itemsMovies:
                    id_movie = movie.get('movie_id')
                    actors = movie.get('actors')
                    directors = movie.get('director')
                    genres_list = movie.get('genres')
                    if id_download == id_movie:
                        actor_list = actors.split(',')
                        directors_list = directors.split(',')
                        for actor in actor_list:
                            act = actor.strip()
                            if act in dict.keys():
                                dict[act] += points_download
                            else:
                                dict[act] = points_download
                        for director in directors_list:
                            dir = director.strip()
                            if dir in dict.keys():
                                dict[dir] += points_download
                            else:
                                dict[dir] = points_download
                        for genre_item in genres_list:
                            gen = genre_item
                            if gen in dict.keys():
                                dict[gen] += points_download
                            else:
                                dict[gen] = points_download

        for reviewItem in itemsReview:
            id_review = reviewItem.get('movie_id')
            rate_review = reviewItem.get('rate')
            user = reviewItem.get('user_id')
            if user_id == user:
                for movie in itemsMovies:
                    id_movie = movie.get('movie_id')
                    actors = movie.get('actors')
                    directors = movie.get('director')
                    genres_list = movie.get('genres')
                    if id_review == id_movie:
                        actor_list = actors.split(',')
                        directors_list = directors.split(',')
                        for actor in actor_list:
                            act = actor.strip()
                            if act in dict.keys():
                                dict[act] += int(rate_review) - 3  # 5 ->2 ... 1 ->-2
                            else:
                                dict[act] = int(rate_review) - 3
                        for director in directors_list:
                            dir = director.strip()
                            if dir in dict.keys():
                                dict[dir] += int(rate_review) - 3
                            else:
                                dict[dir] = int(rate_review) - 3
                        for genre_item in genres_list:
                            gen = genre_item
                            if gen in dict.keys():
                                dict[gen] += int(rate_review) - 3
                            else:
                                dict[gen] = int(rate_review) - 3

        movies_values = {}

        p = 3

        for movie in itemsMovies:
            value_movie = 0
            id_movie = movie.get('movie_id')
            actors = movie.get('actors')
            directors = movie.get('director')
            genres_list = movie.get('genres')
            actors_list = actors.split(",")
            directors_list = directors.split(",")
            date_created = movie.get('date_created')
            for key, value in dict.items():
                for actor in actors_list:
                    ac = actor.strip()
                    if ac == key:
                        value_movie += value
                for director in directors_list:
                    dir = director.strip()
                    if dir == key:
                        value_movie += value
                for genre in genres_list:
                    gen = genre
                    if gen == key:
                        value_movie += value
            given_date = datetime.strptime(date_created, "%Y-%m-%dT%H:%M:%S.%fZ").date()
            today = datetime.utcnow().date()
            three_days_ago = today - timedelta(days=3)
            seven_days_ago = today - timedelta(days=7)
            if given_date == today:
                p = 5
                value_movie *= 3
            if three_days_ago <= given_date < today:
                value_movie *= 2
            if seven_days_ago <= given_date < three_days_ago:
                value_movie *= 1.3
            movies_values[id_movie] = (value_movie, given_date)

        sorted_movies_values = {k: v for k, v in
                                sorted(movies_values.items(), key=lambda item: (item[1][0], -abs(today - item[1][1])),
                                       reverse=True)}

        print(sorted_movies_values)

        interaction_movies_values = {}

        feed_movies_values = []

        for key, value in sorted_movies_values.items():
            a, b = value
            date_str = b.strftime('%Y-%m-%d')
            print(date_str)
            interaction_movies_values[key] = (a, date_str)

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
    except NoCredentialsError as e:
        print("Credentials not available", e)
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Credentials not available'})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
