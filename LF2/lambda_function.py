import json
import os
from time import pthread_getcpuclockid
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
    return {
        'statusCode': 200,
        'body': {
            "uid": uid,
            "items": ITEMS
        }
    }


def post_handler(uid, product):
    # productTable = dynamodb.Table(PRODUCT_TABLE)
    # TODO: check if the product is already in the product table
    # wishlistTable = dynamodb.Table(WISHLIST_TABLE)

    name = product["name"]
    price = product["price"]
    link = product["link"]
    image = product["image"]
    id = link

    # If item not found in Product Table, create it

    response = dynamodb.get_item(
        TableName=PRODUCT_TABLE,
        Key={
            'id': {
                'S': id
            }
        }
    )
    print(response)
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
                'created': {
                    'S': str(datetime.now())
                }
            }
        )
        print('created')

    # response = dynamodb.query(
    #     TableName=WISHLIST_TABLE,
    #     Key={
    #         'uid': {
    #             'S': uid
    #         }
    #     }
    # )

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
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
        'statusCode': 200,
        'body': {
            "uid": uid,
            "item": product
        }
    }


def delete_handler(uid, pid):
    return {
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        },
        'statusCode': 200,
        'body': {
            "uid": uid,
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
