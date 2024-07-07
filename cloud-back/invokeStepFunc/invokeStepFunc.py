import boto3
import os
import json


def invoke_step_func_handler(event, context):
    stepfunctions = boto3.client('stepfunctions')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Or use 'http://localhost:4200/'
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization'
    }

    try:
        state_machine_arn = os.environ['STATE_MACHINE_ARN']
        for record in event['Records']:
            message_body = json.loads(record['body'])
            stepfunctions.start_execution(
                stateMachineArn=state_machine_arn,
                input=json.dumps(message_body)
            )

        return {
            'statusCode': 200,
            'body': json.dumps('Step Function started'),
            'headers': headers
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error starting Step function: {str(e)}')
        }