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


def lambda_handler(event, context):
    # TODO implement LF2

    print(event, context)
    return {
        'statusCode': 200,
        'body': {
            "items": ITEMS
        }
    }
