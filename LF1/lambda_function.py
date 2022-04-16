import json
import requests
import os

ITEMS = [
    {"id": "1", "name": "Kitty 1",
        "image": "https://loremflickr.com/200/200", "price": "50.4", "starred": True},
    {"id": "2", "name": "Kitty 2",
        "image": "https://loremflickr.com/200/200", "price": "20.4", "starred": True},
    {"id": "3", "name": "Kitty 3",
        "image": "https://loremflickr.com/200/200", "price": "54.2", "starred": True},
    {"id": "4", "name": "Kitty 4",
        "image": "https://loremflickr.com/200/200", "price": "50.6", "starred": True},
    {"id": "5", "name": "Kitty 5",
        "image": "https://loremflickr.com/200/200", "price": "35.09", "starred": True},
    {"id": "6", "name": "Kitty 1",
        "image": "https://loremflickr.com/200/200", "price": "50.4", "starred": True},
    {"id": "7", "name": "Kitty 2",
        "image": "https://loremflickr.com/200/200", "price": "20.4", "starred": True},
    {"id": "8", "name": "Kitty 3",
        "image": "https://loremflickr.com/200/200", "price": "54.2", "starred": True},
    {"id": "9", "name": "Kitty 4",
        "image": "https://loremflickr.com/200/200", "price": "50.6", "starred": True},
    {"id": "10", "name": "Kitty 5",
        "image": "https://loremflickr.com/200/200", "price": "35.09", "starred": True},
    {"id": "11", "name": "Kitty 1",
        "image": "https://loremflickr.com/200/200", "price": "50.4", "starred": True},
    {"id": "12", "name": "Kitty 2",
        "image": "https://loremflickr.com/200/200", "price": "20.4", "starred": True},
    {"id": "13", "name": "Kitty 3",
        "image": "https://loremflickr.com/200/200", "price": "54.2", "starred": True},
    {"id": "14", "name": "Kitty 4",
        "image": "https://loremflickr.com/200/200", "price": "50.6", "starred": False},
    {"id": "15", "name": "Kitty 5",
        "image": "https://loremflickr.com/200/200", "price": "35.09", "starred": False},
    {"id": "16", "name": "Kitty 1",
        "image": "https://loremflickr.com/200/200", "price": "50.4", "starred": False},
    {"id": "17", "name": "Kitty 2",
        "image": "https://loremflickr.com/200/200", "price": "20.4", "starred": False},
    {"id": "18", "name": "Kitty 3",
        "image": "https://loremflickr.com/200/200", "price": "54.2", "starred": False},
    {"id": "19", "name": "Kitty 4",
        "image": "https://loremflickr.com/200/200", "price": "50.6", "starred": False},
    {"id": "20", "name": "Kitty 5",
        "image": "https://loremflickr.com/200/200", "price": "35.09", "starred": False},
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


# Unlimited calls per mo
def ebay_call(query):
    """
    Ebay external API call
    Para: query:string
    Return: list of item
        Each item is dict with keys: id(start from idx 1), name, price, image, link
    Latency: 4,193ms
    Pricing: $5.00/mo; Unlimited
    """
    url = "https://ebay-product-search-scraper.p.rapidapi.com/index.php"
    querystring = {"query":query}
    headers = {
    	"X-RapidAPI-Host": "ebay-product-search-scraper.p.rapidapi.com",
    	"X-RapidAPI-Key": os.environ.get('RapidAPIKey')
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    return response['products'][1:]


# IMPORTANT only 200 calls per mo is free!!!
def amazon_call(query):
    """
    Amazon external API call
    Para: query:string
    Return: list of items
        item example
        {
            "isBestSeller": true,
            "product_title": "AMD Ryzen 9 5900X 12-core, 24-Thread Unlocked Desktop Processor",
            "product_main_image_url": "https://m.media-amazon.com/images/I/616VM20+AzL._AC_UY218_.jpg",
            "app_sale_price": "384.10",
            "app_sale_price_currency": "$",
            "isPrime": true,
            "product_detail_url": "https://www.amazon.com/dp/B08164VTWH",
            "product_id": "B08164VTWH",
            "evaluate_rate": "4.8 out of 5 stars",
            "original_price": "$569.99"
        }
    Latency: 8,198ms
    Pricing: $0.00/mo; 200/mo; Hard Limit
    """
    url = "https://amazon24.p.rapidapi.com/api/product"
    # Optional: "categoryID":"aps"
    querystring = {"keyword":query,"country":"US","page":"1"}
    headers = {
    	"X-RapidAPI-Host": "amazon24.p.rapidapi.com",
    	"X-RapidAPI-Key": os.environ.get('RapidAPIKey')
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print("Amazon return:", response.text)
    response = response.json()
    return response['docs']
    
    
def lambda_handler(event, context):
    print(event)
    errors, parsedParams = validate(event)
    if len(errors.keys()) > 0:
        return {
            'statusCode': 400,
            'errors': errors
        }

    q = parsedParams['q']
    sortBy = parsedParams['sort_by']
    
    # External API call
    # Ebay: Unlimited calls
    ebay_items = ebay_call(q)
    
    # Amazon: Only first 200 calls is free!!!
    # amazon_call("notebook")
    
    # TODO: Shopee API, Parse API returns, Add to user search hist db

    # TODO: check if product is in the user's wishlist for logged in users

    return {
        'statusCode': 200,
        'body': {
            "q": q,
            "sort_by": sortBy,
            "count": len(ITEMS),
            "retailers": RETAILERS,
            "items": {
                "Amazon": ITEMS,
                "Ebay": ebay_items,
                "Alibaba": ITEMS,
                "Shopee": ITEMS
            }
        }
    }
