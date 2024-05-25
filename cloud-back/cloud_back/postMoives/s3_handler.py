import json
import boto3



def s3_handler(event, context):

        return {
            'statusCode': 200,
            'body': json.dumps("S3")
        }
