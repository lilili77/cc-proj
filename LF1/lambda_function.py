import json


ITEMS = [
    {pid: 1, name: "Kitty 1" },
    {pid: 2, name: "Kitty 2" },
    {pid: 3, name: "Kitty 3" },
    {pid: 4, name: "Kitty 4" },
]

def lambda_handler(event, context):
    # TODO implement search function
    
    print(event)
    
    return {
        'statusCode': 200,
        'body': {
            count: len(ITEMS)
            items: ITEMS
        }
    }
