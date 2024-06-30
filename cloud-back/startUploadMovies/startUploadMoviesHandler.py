import json
import uuid
import time

import boto3
import os

def upload_data_handler(event, context):
    # Pokretanje Step funkcije
    client = boto3.client('stepfunctions')

    # ARN tvoje Step funkcije koju želiš da pokreneš
    #state_machine_arn = 'arn:aws:states:REGION:ACCOUNT_ID:stateMachine:STATE_MACHINE_NAME'
    state_machine_arn = os.environ['STATE_MACHINE_ARN']

    try:
        if 'body' not in event:
            raise ValueError("Missing body in event")
        body = json.loads(event['body'])
        input_data = {
                'title': body.get('title', ''),
                'description': body.get('description', ''),
                'actors': body.get('actors', ''),
                'director': body.get('director', ''),
                'genres': body.get('genres', ''),
                'name': body.get('name', ''),
                'type': body.get('type', ''),
                'size': body.get('size', ''),
                'date_created': body.get('dateCreated', ''),
                'date_modified': body.get('dateModified', '')
        }


        response = client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_data)

        )





        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Step function completed successfully: {execution_history}.',
                # 'presignedUrl': presigned_url
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error starting Step function: {str(e)}')
        }