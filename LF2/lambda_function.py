import json

def lambda_handler(event, context):
    # TODO implement LF1
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
