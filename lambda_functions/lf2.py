import json
import os
import random

import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from botocore.exceptions import ClientError

REGION = 'us-east-1'
HOST = 'search-restaurants-anrimo223g3nmdgpb5wq3wflwy.us-east-1.es.amazonaws.com'
INDEX = 'restaurants'

def lambda_handler(event, context):
    # TODO implement
    
    # pull message from the SQS queue
    print(">>>polling SQS")
    message = pull_msg_from_sqs()
    if message is None:
        print("the message, if any, wasn't polled")
        return 

    # get the data input from the user
    location = message['Location']
    cuisine = message['Cuisine']
    dining_date = message['DiningDate']
    dining_time = message['DiningTime']
    num_people = message['NumberOfPeople']
    email = message['Email']
    
    print(">>>fetching data from ElasticSearch")
    results = query(cuisine)
    random_restaurant = random.choice(results)
    business_id = random_restaurant['RestaurantID']

    print(">>>looking up the restaurant data in DynamoDB")
    restaurant_data = lookup_data({'business_id': business_id})
    name = restaurant_data['name']
    address = restaurant_data['address']
    address = address.split('[')[1]
    address = address.split(']')[0]
    address = ''.join(address.split("'"))
    zipcode = restaurant_data['zipcode']
    phone = restaurant_data['phone']
    rating = restaurant_data['rating']
    review_count = restaurant_data['review_count']
    cuisine = cuisine
    
    response_to_user = f'''
    Hello,
    I recommend, you check out {name}. It is a {cuisine} restaurant with a rating of {rating} and {review_count} reviews.
    It is located at {address}, and their phone number is {phone}.
    '''
    
    print(response_to_user)
    
    print('>>>sending the response to the user email address')
    send_message_user(email, response_to_user)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'response': 'Email sent to user'})
    }

def pull_msg_from_sqs():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='Q1')
    for message in queue.receive_messages():
        # get the message body
        message_body = json.loads(message.body)
        # delete this message from SQS
        print(">>>deleting message from SQS")
        message.delete()
        return message_body
    return None

    
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
    print(res)
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
                    
                    
def lookup_data(key, db=None, table='yelp-restaurants'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
        print(response['Item'])
        return response['Item']


def send_message_user(email, response_to_user):
    client_sns = boto3.client('sns')
    
    topic_arn = 'arn:aws:sns:us-east-1:064833673922:restaurants'
    print(topic_arn)
    
    subscription_arn = client_sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=email,
        Attributes={
            'FilterPolicy': json.dumps({'email': [email]})
        },
        ReturnSubscriptionArn=True
    )
    print("subscribed: ", subscription_arn['SubscriptionArn'])
    
    response = client_sns.publish(
        TopicArn=topic_arn,
        Message=response_to_user,
        Subject='Dining Concierge Notification',
        MessageAttributes={
            'email': {
                'DataType': 'String',
                'StringValue': email,
            }
        },
    )
    print('email sent: ', response)
    