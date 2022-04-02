import json
import os
import boto3
import base64

def lambda_handler(event, context):
    # TODO implement LF0
    print(event)
    imgBucket = os.environ.get('ImgBucket')
    img_key = event['pathParameters']['imgkey']

    # Alternative way but ContentType is not jpeg
    # img_data = event['body'].encode('ascii')
    # with open("/tmp/imageToSave.jpg", "wb") as fh:
    #     fh.write(base64.decodebytes(img_data))
    # s3 = boto3.client('s3')
    # s3.upload_file('/tmp/imageToSave.jpg', imgBucket, img_key, ExtraArgs={'Metadata': {'Content-Type': 'image/jpeg'}})

    img_data = event['body']
    img_data = base64.b64decode(img_data)
    s3 = boto3.resource('s3')
    s3.Bucket(imgBucket).put_object(Key=img_key, Body=img_data, ContentType='image/jpeg')

    return {
        'statusCode': 200,
        'body': json.dumps('Upload success')
    }
