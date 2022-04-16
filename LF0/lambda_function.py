import json
import os
import boto3
import base64

def lambda_handler(event, context):
    # TODO implement LF0
    
    # Parameters
    imgBucket = os.environ.get('ImgBucket')
    img_key = event['pathParameters']['imgkey']
    img_data = base64.b64decode(event['body'])
    
    # Upload img_key,img_data to s3 bucket imgBucket
    s3 = boto3.resource('s3')
    s3.Bucket(imgBucket).put_object(Key=img_key, Body=img_data, ContentType='image/jpeg')
    
    # Sagemaker Img to embedding
    runtime= boto3.client('runtime.sagemaker')
    payload = json.dumps('{"bucket": "'+ imgBucket +'", "key": "'+ img_key +'"}')
    response = runtime.invoke_endpoint(EndpointName= os.environ['PredictEndPoint'],
                                       ContentType='text/csv',
                                       Body=payload)
    response = json.loads(response['Body'].read().decode())
    print(response)
    
    # Todo Opensearch k-NN search, get corresponding item title from db

    return {
        'statusCode': 200,
        'body': json.dumps('Upload success')
    }
