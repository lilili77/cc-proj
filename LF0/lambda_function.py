import json
import os
import boto3
import base64

from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

def init_search():
    host = 'search-product-embedding-5loh22eno5aldjgq43oxuhvqqi.us-east-1.es.amazonaws.com'
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    
    search = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )
    return search

def lambda_handler(event, context):
    # TODO implement LF0
    
    # Parameters
    imgBucket = os.environ.get('ImgBucket')
    img_key = event['pathParameters']['imgkey']
    img_data = base64.b64decode(event['body'])
    
    # # Upload img_key,img_data to s3 bucket imgBucket
    s3 = boto3.resource('s3')
    s3.Bucket(imgBucket).put_object(Key=img_key, Body=img_data, ContentType='image/jpeg')
    
    # Sagemaker Img to embedding
    runtime= boto3.client('runtime.sagemaker')
    payload = json.dumps({"bucket": imgBucket, "key": img_key}) 
    response = runtime.invoke_endpoint(EndpointName= os.environ['PredictEndPoint'],
                                       ContentType='application/json',
                                       Body=payload)
    response = json.loads(response['Body'].read().decode())
    print(response)
    
    # Openseach k-NN
    search = init_search()
    query = {
      'size': 3,
      'query': {
        'knn': {
          'image-embedding': {
              "vector": response[0],
              "k": 3
          }
        }
      }
    }
    
    response = search.search(
        body=query,
        index="embedding"
    )
    results = response['hits']['hits']
    print(results)
    for result in results:
        print(result['_source']['title'])
    
    # TODO: call LF1 to search title
    

    return {
        'statusCode': 200,
        'body': json.dumps('Upload success')
    }
