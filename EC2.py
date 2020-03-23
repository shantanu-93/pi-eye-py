#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 19:37:50 2020

@author: yoshi
"""

import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAJA3AWTNXX7W2UQAA'
SECRET_KEY = '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'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = upload_to_aws('/Users/yoshi/Downloads/yo.jpeg', 'contentbucket546', 'test data')

bucketname = 'contentbucket546' # replace with your bucket name
filename = 'test data' # replace with your object key
s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
s3.Bucket(bucketname).download_file(filename, 'test1.jpg')

region_name = "us-east-1"
# Create SQS client
sqs = boto3.client('sqs', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,region_name=region_name)

queue_url = 'https://queue.amazonaws.com/684896435815/videos_queue'

length = 0

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)
print(response)

message = response['Messages'][0]
# receipt_handle = message['ReceiptHandle']

# Delete received message from queue
sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)
length = len(response['Messages'])
print('Received and deleted message: %s' % message)