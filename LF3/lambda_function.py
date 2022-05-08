import os
import boto3


SearchHistoryTable = os.environ.get('SearchHistoryTable')
dynamodb = boto3.client('dynamodb')

VALID_METHODS = ["GET", "SEARCH"]


def validate(params):
    uid = params["uid"]
    method = params["method"]

    errors = {}
    parsedParams = {
        "uid": uid,
        "method": method,
    }

    if method not in VALID_METHODS:
        errors["method"] = f"'method' must be one of {VALID_METHODS}"
    if uid == "":
        errors["uid"] = "'uid' can't be empty"

    if method == "SEARCH":
        query = params["q"]
        parsedParams["q"] = query
        if query == "":
            errors["q"] = "'q' can't be empty"

    return errors, parsedParams


def get_search_history(uid):
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
        searchHistory.append(
            (item['q']['S'], item['datetime']['S'], item['img']['S']))

    return {
        'statusCode': 200,
        'body': {
            "items": searchHistory
        }
    }


def search_search_history(uid, q):
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

    if "Items" not in response or len(response["Items"]) == 0:
        return EMPTY

    items = response["Items"]
    filtered_items = []
    for item in items:
        if q.lower() in item['q']['S'].lower():
            filtered_items.append(item)

    if not filtered_items:
        return EMPTY

    return {
        'statusCode': 200,
        'body': {
            "items": filtered_items
        }
    }


def lambda_handler(event, context):
    errors, parsedParams = validate(event)
    if len(errors.keys()) > 0:
        return {
            'statusCode': 400,
            'errors': errors
        }

    uid = parsedParams["uid"]
    method = parsedParams["method"]

    if method == "GET":
        return get_search_history(uid)
    elif method == "SEARCH":
        query = parsedParams["q"]
        return search_search_history(uid, query)
