import json

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


def lambda_handler(event, context):
    # TODO implement search function
    q = event['q']

    return {
        'statusCode': 200,
        'body': {
            "q": q,
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
