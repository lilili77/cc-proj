import os
import boto3

VALID_METHODS = ["GET", "POST", "DELETE"]
dynamodb = boto3.client('dynamodb')

PRODUCT_TABLE = os.environ.get('ProductTable')
PRICE_HISTORY_TABLE = os.environ.get('PriceHistoryTable')

print(PRODUCT_TABLE, PRICE_HISTORY_TABLE)


def validate(params):
    pid = params["pid"]

    errors = {}
    parsedParams = {
        "pid": pid
    }

    if pid == "":
        errors["pid"] = "'pid' can't be empty"

    return errors, parsedParams


def parse_item(item):
    created = item['created']['S']
    image = item['image']['S']
    link = item['link']['S']
    name = item['name']['S']
    price = item['price']['N']
    retailer = item['retailer']['S']
    id = item['id']['S']

    return {
        "id": id,
        "created": created,
        "image": image,
        "link": link,
        "name": name,
        "price": price,
        "retailer": retailer,
    }


def get_product_detail(pid):
    response = dynamodb.get_item(
        TableName=PRODUCT_TABLE,
        Key={
            'id': {
                'S': pid
            }
        }
    )

    if "Item" not in response:
        return None

    print(response)
    return parse_item(response["Item"])


def get_price_histry(pid):
    pass


def lambda_handler(event, context):
    errors, parsedParams = validate(event)
    if len(errors.keys()) > 0:
        return {
            'statusCode': 400,
            'errors': errors
        }

    pid = parsedParams["pid"]
    print('pid', pid)

    detail = get_product_detail(pid)

    return {
        'statusCode': 200,
        'body': {
            'product': detail,
            'price_history': []
        }
    }
