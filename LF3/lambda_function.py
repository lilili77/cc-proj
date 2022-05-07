import requests
import os
import boto3


SearchHistoryTable = os.environ.get('SearchHistoryTable')
dynamodb = boto3.client('dynamodb')

def get_search_hist(uid):
    response = dynamodb.query(
        TableName=SearchHistoryTable,
        KeyConditionExpression='uid = :v1',
        ExpressionAttributeValues={
            ':v1': {
                'S': uid
            }
        }
    )
    
    # searchHistory is a list of tuple (q,datetime,imgKey)
    searchHistory = []
    for item in response['Items']:
        searchHistory.append((item['q']['S'],item['datetime']['S'],item['imgKey']['S']))
    print(searchHistory)
    
    return {
        'statusCode': 200,
        'items': searchHistory
    }


def search_search_hist(uid,q):
    EMPTY = {
        'statusCode': 200,
        'body': {
            'items': []
        }
    }
    # Find products in user's wishlist
    response = dynamodb.query(
        TableName=SearchHistoryTable,
        KeyConditionExpression='uid = :v1',
        ExpressionAttributeValues={
            ':v1': {
                'S': uid
            }
        }
    )
    
    print("response",response)

    if "Items" not in response or len(response["Items"]) == 0:
        return EMPTY
        
    items = response["Items"]
    filtered_items = []
    for item in items:
        if q.lower() in item['q']['S'].lower():
            filtered_items.append(item)
    print("filtered_items",filtered_items)
    
    if not filtered_items:
        return EMPTY
    
    return {
        'statusCode': 200,
        'body': {
            "items": filtered_items
        }
    }
    

def lambda_handler(event, context):
    # TODO: Get uid, q and path from API call then parse

    uid = '084d4246-b6fe-402b-9da4-0a6e95335700'
    q = 'vic'
    
    # Get search history
    # return get_search_hist(uid)
    
    # Search search history
    return search_search_hist(uid,q)