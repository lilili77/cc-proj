import json


ITEMS = [
    {"id": "1", "name": "Kitty 1",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.4", "created": '2022-03-10'},
    {"id": "2", "name": "Kitty 2",
        "imageUrl": "https://loremflickr.com/200/200", "price": "20.4", "created": '2022-03-10'},
    {"id": "3", "name": "Kitty 3",
        "imageUrl": "https://loremflickr.com/200/200", "price": "54.2", "created": '2022-03-10'},
    {"id": "4", "name": "Kitty 4",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.6", "created": '2022-03-26'},
    {"id": "5", "name": "Kitty 5",
        "imageUrl": "https://loremflickr.com/200/200", "price": "35.09", "created": '2022-03-25'},
    {"id": "6", "name": "Kitty 1",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.4", "created": '2022-03-25'},
    {"id": "7", "name": "Kitty 2",
        "imageUrl": "https://loremflickr.com/200/200", "price": "20.4", "created": '2022-03-25'},
    {"id": "8", "name": "Kitty 3",
        "imageUrl": "https://loremflickr.com/200/200", "price": "54.2", "created": '2022-03-25'},
    {"id": "9", "name": "Kitty 4",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.6", "created": '2022-03-15'},
    {"id": "10", "name": "Kitty 5",
        "imageUrl": "https://loremflickr.com/200/200", "price": "35.09", "created": '2022-03-26'},
    {"id": "11", "name": "Kitty 1",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.4", "created": '2022-03-26'},
    {"id": "12", "name": "Kitty 2",
        "imageUrl": "https://loremflickr.com/200/200", "price": "20.4", "created": '2022-03-26'},
    {"id": "13", "name": "Kitty 3",
        "imageUrl": "https://loremflickr.com/200/200", "price": "54.2", "created": '2022-03-25'},
    {"id": "14", "name": "Kitty 4",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.6", "created": '2022-04-01'},
    {"id": "15", "name": "Kitty 5",
        "imageUrl": "https://loremflickr.com/200/200", "price": "35.09", "created": '2022-04-01'},
    {"id": "16", "name": "Kitty 1",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.4", "created": '2022-04-01'},
    {"id": "17", "name": "Kitty 2",
        "imageUrl": "https://loremflickr.com/200/200", "price": "20.4", "created": '2022-04-02'},
    {"id": "18", "name": "Kitty 3",
        "imageUrl": "https://loremflickr.com/200/200", "price": "54.2", "created": '2022-04-03'},
    {"id": "19", "name": "Kitty 4",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.6", "created": '2022-04-03'},
    {"id": "20", "name": "Kitty 5",
        "imageUrl": "https://loremflickr.com/200/200", "price": "35.09", "created": '2022-04-03'},
]

VALID_METHODS = ["GET", "POST", "DELETE"]


def validate(params):
    uid = params["uid"]
    method = params["method"]

    errors = {}
    parsedParams = {
        "uid": uid,
        "method": method
    }

    if method not in VALID_METHODS:
        errors["method"] = f"'method' must be one of {VALID_METHODS}"
    if uid == "":
        errors["uid"] = "'uid' can't be empty"

    if method == "POST":
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


def post_handler(uid):
    return {
        'statusCode': 200,
        'body': {
            "uid": uid,
            "item": {}
        }
    }


def delete_handler(uid, pid):
    return {
        'statusCode': 200,
        'body': {
            "uid": uid,
            "item": {}
        }
    }


def lambda_handler(event, context):
    print(event, context)

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
        return post_handler(uid)
    if method == "DELETE":
        pid = parsedParams["pid"]
        return delete_handler(uid)

    return {
        'statusCode': 200,
        'body': "hi"
    }
