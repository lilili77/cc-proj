import requests
import os
import boto3
from bs4 import BeautifulSoup
from datetime import date


dynamodb = boto3.client('dynamodb')

PRODUCT_TABLE = os.environ.get('ProductTable')
PRODUCTHISTORY_TABLE = os.environ.get('PriceHistoryTable')


def get_price(url):
    # http = urllib3.PoolManager()
    # response = http.request('GET', url)
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, features="html.parser")
    soup.prettify()
    if soup is None:
        return None
    price = soup.find(id="prcIsum")
    print(price)
    if price is not None and "content" in str(price):
        price = price["content"]
        return float(price)
    else:
        return None


def lambda_handler(event, context):
    # TODO: Get price and update price history

    response = dynamodb.scan(TableName=PRODUCT_TABLE)
    products = response["Items"]
    today = str(date.today())

    for product in products:
        print("here")
        retailer = product["retailer"]["S"]
        if retailer == "Ebay":
            print(product)
            url = product["link"]["S"]
            id = product["id"]["S"]
            old_price = product["price"]["N"]
            price = get_price(url)
            print(price)
            if price is None:
                print(url)
                continue

            # price_hist = product["price_history"]["SS"]
            # price_hist.append(str(price))
            # print(price_hist)
            # price_date = product["price_date"]["SS"]
            # price_date.append(str(today))

            update_item = {"price": {"Value": {"S": price}}}
            # dynamodb.update_item(TableName=PRODUCT_TABLE, Key=key, AttributeUpdates=update_item)
            item_attr = {
                'pid': {
                    'S': id
                },
                'date': {
                    'S': today
                },
                'price': {
                    'N': str(price)
                }

            }
            print("item", item_attr)

            dynamodb.put_item(TableName=PRODUCTHISTORY_TABLE, Item=item_attr)
        

    return {
        'statusCode': 200,
        'body': "Hello"
    }

