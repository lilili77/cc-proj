import requests
import os
import boto3


SearchHistoryTable = os.environ.get('SearchHistoryTable')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO: Return search history

    # Parameter
    uid = '10356ed1-d26b-41f3-b940-5111ecc194de'
    
    response = dynamodb.query(
        TableName=SearchHistoryTable,
        KeyConditionExpression='uid = :v1',
        ExpressionAttributeValues={
            ':v1': {
                'S': uid
            }
        }
    )
    
    # list of tuple (q,datetime,imgKey)
    searchHistory = []
    for item in response['Items']:
        searchHistory.append((item['q']['S'],item['datetime']['S'],item['imgKey']['S']))
    print(searchHistory)
        

    return {
        'statusCode': 200,
        'body': "Hello"
    }
