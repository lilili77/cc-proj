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


def lambda_handler(event, context):
    errors, parsedParams = validate(event)
    if len(errors.keys()) > 0:
        return {
            'statusCode': 400,
            'errors': errors
        }

    pid = parsedParams["pid"]
    print('pid', pid)

    return {
        'statusCode': 200,
        'body': {
            'product': {
                'id': pid,
                'name': 'yes',
            },
            'price_history': []
        }
    }
