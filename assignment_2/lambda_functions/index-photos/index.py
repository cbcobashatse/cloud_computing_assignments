import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from datetime import datetime

def is_valid_json(json_string):
    try:
        json.loads(json_string)
    except ValueError:
        return False
    return True

def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    # Create an S3 client
    s3_client = boto3.client('s3')

    # Call the head_object method to retrieve the object's metadata
    response = s3_client.head_object(Bucket=s3_bucket, Key=s3_key)
    print(response)

    # Retrieve the custom labels from the metadata, if applicable
    custom_labels_str = response.get('Metadata', {}).get('customlabels', '')
    print(custom_labels_str)
    custom_labels = custom_labels_str.split(', ') if custom_labels_str else []
    print(custom_labels)

    # Create a Rekognition client
    rekognition_client = boto3.client('rekognition')

    # Call the detectLabels method to detect labels in the image
    response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': s3_bucket,
                'Name': s3_key
            }
        },
        MaxLabels=10,
        MinConfidence=80
    )

    # Append the detected labels to the custom labels array
    for label in response['Labels']:
        custom_labels.append(label['Name'])

    # Create an OpenSearch client
    host = 'search-photos-li3ftss63u7d26i25zryut4ayy.us-east-1.es.amazonaws.com'
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    aws_auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    es_client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=aws_auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    # Format the current datetime in ISO 8601 format
    created_timestamp = response.get('LastModified', None)

    # Create a JSON document to index in OpenSearch
    doc = {
        'objectKey': s3_key,
        'bucket': s3_bucket,
        'createdTimestamp': created_timestamp,
        'labels': custom_labels
    }

    # Index the document in the "photos" index
    es_client.index(index='photos', body=doc)
    
    # Print the custom labels and the detected labels to the console
    print('Custom labels:', custom_labels)
    print('timestamp: ', created_timestamp)
    print('Detected labels:')
    for label in response['Labels']:
        print(label['Name'])
        
    # Prepare the response object
    response_frontend = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps('Photo successfully uploaded and indexed!')
    }
    
    return response_frontend