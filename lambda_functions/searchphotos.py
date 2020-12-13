import json
import os
import math
import dateutil.parser
import datetime
import time
import logging
import boto3
import requests
from requests.auth import HTTPBasicAuth


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    
    return response

    
def lambda_handler(event, context):
    # TODO implement
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    client = boto3.client('lex-runtime')
    response_lex = client.post_text(
    botName='photo',
    botAlias="photo",
    userId="test",
    #inputText= "photo with boy")
    inputText= event["queryStringParameters"]['q'])
    
    print(response_lex)
    if 'slots' in response_lex:
        if 'slotTwo' in response_lex['slots']:
            keys = [response_lex['slots']['slotOne'],response_lex['slots']['slotTwo']]
        else:
            keys = [response_lex['slots']['slotOne']]
        pictures = search_intent(keys) #get images keys from elastic search labels
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(pictures),
            "isBase64Encoded": False
        }
    else:
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": [],
            "isBase64Encoded": False}
    return response
    
def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    return search_intent(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')

def search_intent(labels):
    url = 'https://vpc-photos-rkvuigox7og7d7lervybnntmie.us-west-2.es.amazonaws.com/_search?q='
    resp = []
    for label in labels:
        if (label is not None) and label != '':
            url2 = url+label
            resp.append(requests.get(url2, auth = HTTPBasicAuth('kiyoon', 'KIwi727272!')).json())
    print (resp)
  
    output = []
    for r in resp:
        if 'hits' in r:
             for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                if key not in output:
                    output.append(key)
    print(output)

    return output
