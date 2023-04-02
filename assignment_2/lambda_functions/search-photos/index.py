import json
import os
import boto3
import time
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

REGION = 'us-east-1'
HOST = 'search-photos-li3ftss63u7d26i25zryut4ayy.us-east-1.es.amazonaws.com'
INDEX = 'photos'

# Define the client to interact with Lex
client = boto3.client('lexv2-runtime')
def lambda_handler(event, context):
    
    queryStringParams = event.get('queryStringParameters')
    param_values_str = ''
    if queryStringParams:
        for param in queryStringParams:
            param_values_str = ', '.join(queryStringParams.values())
        print(param_values_str)
    
    message = param_values_str
    session_id = 'testuser_' + str(time.time())
    response = client.recognize_text(
            botId='92X6V1TIW7',
            botAliasId='TSTALIASID',
            localeId='en_US',
            sessionId=session_id,
            text=message)
    msg_from_lex = response.get('messages', [])
    sessionState = response.get('sessionState')
    slots = sessionState['intent']['slots']
    print(slots)
    results = []
    
    if slots['item1'] is not None:
        keyword = slots['item1']['value']['interpretedValue']
        singular_keyword = singularize(keyword)
        result1 = query(singular_keyword)
        for obj in result1:
            results.append(obj)
    if slots['item2'] is not None:
        keyword = slots['item2']['value']['interpretedValue']
        singular_keyword = singularize(keyword)
       
        result2 = query(singular_keyword)
        for obj in result2:
            results.append(obj)
    
    print(results)
    
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(results)
        # "body": json.dumps({"results": results})
    }
    return response
    
def singularize(word):
    if word.endswith('s'):
        return word[:-1]
    else:
        return word
    
    
def query(term):
    client = OpenSearch(hosts=[{
        'host': HOST,
        'port': 443
    }],
                        http_auth=get_awsauth(REGION, 'es'),
                        use_ssl=True,
                        verify_certs=True,
                        connection_class=RequestsHttpConnection)
                        
    # query body to get the total size
    q = {'size': 1, 'query': {'multi_match': {'query': term}}}
    res = client.search(index=INDEX, body=q)
    total_size = res['hits']['total']['value']
    
    # actual query to get the values
    q = {'size': total_size, 'query': {'multi_match': {'query': term}}}
    res = client.search(index=INDEX, body=q)
    #print(res)
    # print("total: ", total_size)
    # print("returned: ", len(res['hits']['hits']))

    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    return results
    


def get_awsauth(region, service):
    cred = boto3.Session().get_credentials()
    return AWS4Auth(cred.access_key,
                    cred.secret_key,
                    region,
                    service,
                    session_token=cred.token)









