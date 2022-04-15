import json
import requests
import os

ITEMS = [
    {"id": "1", "name": "Kitty 1",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.4", "starred": True},
    {"id": "2", "name": "Kitty 2",
        "imageUrl": "https://loremflickr.com/200/200", "price": "20.4", "starred": True},
    {"id": "3", "name": "Kitty 3",
        "imageUrl": "https://loremflickr.com/200/200", "price": "54.2", "starred": True},
    {"id": "4", "name": "Kitty 4",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.6", "starred": True},
    {"id": "5", "name": "Kitty 5",
        "imageUrl": "https://loremflickr.com/200/200", "price": "35.09", "starred": True},
    {"id": "6", "name": "Kitty 1",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.4", "starred": True},
    {"id": "7", "name": "Kitty 2",
        "imageUrl": "https://loremflickr.com/200/200", "price": "20.4", "starred": True},
    {"id": "8", "name": "Kitty 3",
        "imageUrl": "https://loremflickr.com/200/200", "price": "54.2", "starred": True},
    {"id": "9", "name": "Kitty 4",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.6", "starred": True},
    {"id": "10", "name": "Kitty 5",
        "imageUrl": "https://loremflickr.com/200/200", "price": "35.09", "starred": True},
    {"id": "11", "name": "Kitty 1",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.4", "starred": True},
    {"id": "12", "name": "Kitty 2",
        "imageUrl": "https://loremflickr.com/200/200", "price": "20.4", "starred": True},
    {"id": "13", "name": "Kitty 3",
        "imageUrl": "https://loremflickr.com/200/200", "price": "54.2", "starred": True},
    {"id": "14", "name": "Kitty 4",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.6", "starred": False},
    {"id": "15", "name": "Kitty 5",
        "imageUrl": "https://loremflickr.com/200/200", "price": "35.09", "starred": False},
    {"id": "16", "name": "Kitty 1",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.4", "starred": False},
    {"id": "17", "name": "Kitty 2",
        "imageUrl": "https://loremflickr.com/200/200", "price": "20.4", "starred": False},
    {"id": "18", "name": "Kitty 3",
        "imageUrl": "https://loremflickr.com/200/200", "price": "54.2", "starred": False},
    {"id": "19", "name": "Kitty 4",
        "imageUrl": "https://loremflickr.com/200/200", "price": "50.6", "starred": False},
    {"id": "20", "name": "Kitty 5",
        "imageUrl": "https://loremflickr.com/200/200", "price": "35.09", "starred": False},
]


RETAILERS = [
    {"name": "Amazon", "url": "https://amazon.com"},
    {"name": "Ebay", "url": "https://ebay.com"},
    {"name": "Alibaba", "url": "https://alibaba.com"},
    {"name": "Shopee", "url": "https://shopee.com"},
]

VALID_SORTBY = ['price', 'relevance']


def validate(params):
    q = params['q']
    sort_by = params['sort_by']
    parsedParams = {
        "q": q,
        "sort_by": "price"
    }
    errors = {}

    if q == "":
        errors["q"] = "'q' can't be empty"
    if sort_by != "":
        if sort_by not in VALID_SORTBY:
            errors["sort_by"] = f"'sort_by' must be one of {VALID_SORTBY}"
        else:
            parsedParams["sort_by"] = sort_by

    return errors, parsedParams

def ebay_call(query):
    """
    Ebay external API call
    Para: query:string
    Return: list of item
        Each item is dict with keys: id(start from idx 1), name, price, image, link
    Latency: 4,193ms
    """
    url = "https://ebay-product-search-scraper.p.rapidapi.com/index.php"
    querystring = {"query":query}
    headers = {
    	"X-RapidAPI-Host": "ebay-product-search-scraper.p.rapidapi.com",
    	"X-RapidAPI-Key": os.environ.get('RapidAPIKey')
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print("Ebay return:", response.text)
    response = response.json()
    return response['products'][1:]

def lambda_handler(event, context):
    # TODO implement search function
    print(event)
    errors, parsedParams = validate(event)
    if len(errors.keys()) > 0:
        return {
            'statusCode': 400,
            'errors': errors
        }

    q = parsedParams['q']
    sortBy = parsedParams['sort_by']
    
    # Ebay API call
    ebay_call("gpu")

    return {
        'statusCode': 200,
        'body': {
            "q": q,
            "sort_by": sortBy,
            "count": len(ITEMS),
            "retailers": RETAILERS,
            "items": {
                "Amazon": ITEMS,
                "Ebay": ITEMS,
                "Alibaba": ITEMS,
                "Shopee": ITEMS
            }
        }
    }
