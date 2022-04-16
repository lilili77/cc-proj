import os
import boto3
from datetime import datetime

ITEMS = [
    {"id": "1", "name": "Kitty 1", "image": "https://loremflickr.com/200/200",
        "price": "50.4", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "2", "name": "Kitty 2", "image": "https://loremflickr.com/200/200",
        "price": "20.4", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "3", "name": "Kitty 3", "image": "https://loremflickr.com/200/200",
        "price": "54.2", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "4", "name": "Kitty 4", "image": "https://loremflickr.com/200/200",
        "price": "50.6", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "5", "name": "Kitty 5", "image": "https://loremflickr.com/200/200",
        "price": "35.09", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "6", "name": "Kitty 1", "image": "https://loremflickr.com/200/200",
        "price": "50.4", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "7", "name": "Kitty 2", "image": "https://loremflickr.com/200/200",
        "price": "20.4", "link": "https://amazon.com/", "created": '2022-03-11'},
    {"id": "8", "name": "Kitty 3", "image": "https://loremflickr.com/200/200",
        "price": "54.2", "link": "https://amazon.com/", "created": '2022-03-12'},
    {"id": "9", "name": "Kitty 4", "image": "https://loremflickr.com/200/200",
        "price": "50.6", "link": "https://amazon.com/", "created": '2022-03-13'},
    {"id": "10", "name": "Kitty 5", "image": "https://loremflickr.com/200/200",
        "price": "35.09", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "11", "name": "Kitty 1", "image": "https://loremflickr.com/200/200",
        "price": "50.4", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "12", "name": "Kitty 2", "image": "https://loremflickr.com/200/200",
        "price": "20.4", "link": "https://amazon.com/", "created": '2022-03-14'},
    {"id": "13", "name": "Kitty 3", "image": "https://loremflickr.com/200/200",
        "price": "54.2", "link": "https://amazon.com/", "created": '2022-03-15'},
    {"id": "14", "name": "Kitty 4", "image": "https://loremflickr.com/200/200",
        "price": "50.6", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "15", "name": "Kitty 5", "image": "https://loremflickr.com/200/200",
        "price": "35.09", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "16", "name": "Kitty 1", "image": "https://loremflickr.com/200/200",
        "price": "50.4", "link": "https://amazon.com/", "created": '2022-03-13'},
    {"id": "17", "name": "Kitty 2", "image": "https://loremflickr.com/200/200",
        "price": "20.4", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "18", "name": "Kitty 3", "image": "https://loremflickr.com/200/200",
        "price": "54.2", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "19", "name": "Kitty 4", "image": "https://loremflickr.com/200/200",
        "price": "50.6", "link": "https://amazon.com/", "created": '2022-03-10'},
    {"id": "20", "name": "Kitty 5", "image": "https://loremflickr.com/200/200",
        "price": "35.09", "link": "https://amazon.com/", "created": '2022-03-10'},
]


VALID_METHODS = ["GET", "POST", "DELETE"]
dynamodb = boto3.client('dynamodb')

WISHLIST_TABLE = os.environ.get('WishlistTable')
PRODUCT_TABLE = os.environ.get('ProductTable')


def parseItem(item):
    created = item['created']['S']
    image = item['image']['S']
    link = item['link']['S']
    name = item['name']['S']
    price = item['price']['N']
    retailer = item['retailer']['S']

    return {
        "created": created,
        "image": image,
        "link": link,
        "name": name,
        "price": price,
        "retailer": retailer,
    }


def validate(params):
    print(params)
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

    if method == "POST":
        item = params["item"]
        parsedParams["item"] = item
        # TODO: body error validation

    if method == "DELETE":
        pid = params["pid"]
        parsedParams["pid"] = pid
        if pid == "":
            errors["pid"] = "'pid' can't be empty"

    return errors, parsedParams


def get_handler(uid):
    EMPTY = {
        'statusCode': 200,
        'body': {
            'items': []
        }
    }
    # Find products in user's wishlist
    response = dynamodb.query(
        TableName=WISHLIST_TABLE,
        KeyConditionExpression='uid = :v1',
        ExpressionAttributeValues={
            ':v1': {
                'S': uid
            }
        }
    )

    if "Items" not in response or len(response["Items"]) == 0:
        return EMPTY

    # Get details of all products from product table
    items = response["Items"]
    keys = list(map(lambda item: {'id': {'S': item['pid']['S']}}, items))

    response = dynamodb.batch_get_item(
        RequestItems={
            PRODUCT_TABLE: {
                'Keys': keys
            }
        }
    )

    response = response['Responses']

    if PRODUCT_TABLE not in response:
        return EMPTY

    items = response[PRODUCT_TABLE]

    return {
        'statusCode': 200,
        'body': {
            "uid": uid,
            "items": list(map(lambda item: parseItem(item), items))
        }
    }


def post_handler(uid, product):
    image = product["image"]
    link = product["link"]
    name = product["name"]
    price = product["price"]
    retailer = product["retailer"]
    id = link

    # Make sure product is in Product Table. If not, create it
    response = dynamodb.get_item(
        TableName=PRODUCT_TABLE,
        Key={
            'id': {
                'S': id
            }
        }
    )

    if "Item" not in response:
        dynamodb.put_item(
            TableName=PRODUCT_TABLE,
            Item={
                'id': {
                    'S': id
                },
                'name': {
                    'S': name
                },
                'price': {
                    'N': price
                },
                'link': {
                    'S': link
                },
                'image': {
                    'S': image
                },
                'retailer': {
                    'S': retailer
                },
                'created': {
                    'S': str(datetime.now())
                }
            }
        )

    response = dynamodb.query(
        TableName=WISHLIST_TABLE,
        KeyConditionExpression='uid = :v1 AND pid = :v2',
        ExpressionAttributeValues={
            ':v1': {
                'S': uid
            },
            ':v2': {
                'S': id
            }
        }
    )

    if "Item" in response:
        return {
            'statusCode': 400,
            'error': "Product is already in user's wishlist."
        }

    dynamodb.put_item(
        TableName=WISHLIST_TABLE,
        Item={
            'uid': {
                'S': uid
            },
            'pid': {
                'S': id
            },
            'created': {
                'S': str(datetime.now())
            }
        }
    )

    return {
        'statusCode': 200,
        'body': {
            "item": product
        }
    }


def delete_handler(uid, pid):
    dynamodb.delete_item(
        TableName=WISHLIST_TABLE,
        Key={
            'uid': {
                'S': uid
            },
            'pid': {
                'S': pid
            }
        }
    )

    return {
        'statusCode': 200,
        'body': {
            "item": {}
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
        return get_handler(uid)
    if method == "POST":
        product = parsedParams["item"]
        return post_handler(uid, product)
    if method == "DELETE":
        pid = parsedParams["pid"]
        return delete_handler(uid, pid)

    return {
        'statusCode': 200,
        'body': "hi"
    }
