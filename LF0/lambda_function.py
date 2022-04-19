import json
import os
import uuid
import boto3
import base64

from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

import spacy
from string import punctuation
from collections import Counter


def init_search():
    '''
    Initialize opensearch
    '''
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

# Klayers-python38-spacy layer deprecated 2022-08-04T04:59:13
def extract_keywords(text):
    '''
    Extract Proper NOUN, Adjective, NOUN from given text (matched titles combined)
    Return: a list of 5 most frequent words
    '''
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    nlp = spacy.load("/opt/en_core_web_sm-2.2.5/en_core_web_sm/en_core_web_sm-2.2.5")
    doc = nlp(text.lower())
    
    result = []
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    
    result = [x[0] for x in Counter(result).most_common(5)]
    print('Extract keywords',result)
    return result

def lambda_handler(event, context):
    # TODO implement LF0

    # Parameters
    IMG_BUCKET = os.environ.get('ImgBucket')
    img_key = str(uuid.uuid1())
    public_img_key = f"public/{img_key}"
    img_data = base64.b64decode(event['body'])
    content_type = 'image/jpeg' #event['headers']['content-type'] fix upload bug

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
    print(response) # the embedding

    # Openseach k-NN to get a list of title of matching img
    search = init_search()
    num_match = 3
    query = {
        'size': num_match,
        'query': {
            'knn': {
                'image-embedding': {
                    'vector': response[0],
                    'k': num_match
                }
            }
        }
    }
    response = search.search(
        body=query,
        index='embedding'
    )
    results = response['hits']['hits']
    # create title list
    title_lst = []
    print('Matched titles:')
    for result in results:
        print(result['_source']['title'])
        title_lst.append(result['_source']['title'])
    
    # Keyword extraction from title list
    text = ' '.join(title_lst)
    title = ' '.join(extract_keywords(text))

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
