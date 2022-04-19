import json
import os
import uuid
import boto3
import base64

from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

import spacy

def init_search():
    host = os.environ['OpensearchEndPoint']
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                       region, service, session_token=credentials.token)

    search = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    return search

def extract_keywords(text):
    
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())
    
    result = []
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    print(Counter(result).most_common(5))
    result = [x[0] for x in Counter(result).most_common(5)]
    return result

def lambda_handler(event, context):
    # TODO implement LF0

    # Parameters
    IMG_BUCKET = os.environ.get('ImgBucket')
    img_key = str(uuid.uuid1())
    public_img_key = f"public/{img_key}"
    img_data = base64.b64decode(event['body'])
    content_type = 'image/jpeg' #event['headers']['content-type']

    # Upload img_key,img_data to s3 bucket IMG_BUCKET
    s3 = boto3.resource('s3')
    # Must put in public/ folder for frontend access
    s3.Bucket(IMG_BUCKET).put_object(
        Key=public_img_key, Body=img_data, ContentType=content_type)

    # Sagemaker Img to embedding
    runtime = boto3.client('runtime.sagemaker')
    payload = json.dumps({'bucket': IMG_BUCKET, 'key': public_img_key})
    response = runtime.invoke_endpoint(EndpointName=os.environ['PredictEndPoint'],
                                       ContentType='application/json',
                                       Body=payload)
    response = json.loads(response['Body'].read().decode())
    print(response)

    # Openseach k-NN to get a list of title
    search = init_search()
    query = {
        'size': 3,
        'query': {
            'knn': {
                'image-embedding': {
                    'vector': response[0],
                    'k': 3
                }
            }
        }
    }
    response = search.search(
        body=query,
        index='embedding'
    )
    results = response['hits']['hits']
    title_lst = []
    for result in results:
        title_lst.append(result['_source']['title'])
    
    # Keyword extraction from title list
    text = '.'.join(title_lst)
    extract_keywords(text)
    

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        # return the first title
        'body': json.dumps({
            # return the first title
            'title': results[0]['_source']['title'],
            'key': img_key,
            'bucket': IMG_BUCKET
        })
    }
