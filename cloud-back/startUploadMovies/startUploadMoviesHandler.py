import json
import uuid

import boto3
import os

def upload_data_handler(event, context):
    # Pokretanje Step funkcije
    client = boto3.client('stepfunctions')

    # ARN tvoje Step funkcije koju želiš da pokreneš
    #state_machine_arn = 'arn:aws:states:REGION:ACCOUNT_ID:stateMachine:STATE_MACHINE_NAME'
    state_machine_arn = os.environ['STATE_MACHINE_ARN']

    # Input za Step funkciju (opciono)
    input_data = {
        'key1': 'value1',
        'key2': 'value2'
    }

    try:
        response = client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input_data)
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Step function started successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error starting Step function: {str(e)}')
        }