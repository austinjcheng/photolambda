import json
import boto3
import requests
import time
from requests.auth import HTTPBasicAuth

def lambda_handler(event, context):
    
    print(event)
    print("hello22")
    print("checkifitupdates")
    print("doublecheck")
    client = boto3.client('rekognition')
    s3_info = event['Records'][0]['s3']
    bucket = s3_info['bucket']['name']
    key = s3_info['object']['key']
    print(bucket)
    print(key)

    pass_object = {'S3Object':{'Bucket':bucket,'Name':key}}
    resp = client.detect_labels(Image=pass_object,MaxLabels=10)
    timestamp =time.time()
    labels = []
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    format = {'objectKey':key,'bucket':bucket,'createdTimestamp':timestamp,'labels':labels}
    required_json = json.dumps(format)
    print(required_json)
    url = "https://vpc-photos-rkvuigox7og7d7lervybnntmie.us-west-2.es.amazonaws.com/photos/0"
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers, auth=HTTPBasicAuth('kiyoon', 'KIwi727272!'))
    print(r.text)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
