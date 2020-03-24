import boto3
from global_constants import GlobalConstants
import time
const = GlobalConstants()

# SQS client
# max_queue_messages = 10
# message_bodies = []
sqs = boto3.client('sqs'
        , region_name=GlobalConstants().REGION,
        aws_access_key_id=GlobalConstants().ACCESS_KEY,
        aws_secret_access_key=GlobalConstants().SECRET_KEY)


# Create a queue
def create_queue(q_name, delay_sec = None, retention_pd = None):
    response = sqs.create_queue(
        QueueName=q_name,
        Attributes={
            # 'DelaySeconds': '60' if delay_sec is None else str(delay_sec),
            # 'MessageRetentionPeriod': '86400' if retention_pd is None else str(retention_pd),
            'FifoQueue': 'true',
            'ContentBasedDeduplication ' : 'true'
        }
    )
    print(response['QueueUrl'])
    # return response['QueueUrl']

def update_queue(q_name, attribute, value):
    queue_url = get_queue_url(q_name)
    sqs.set_queue_attributes(
    QueueUrl=queue_url,
    Attributes={attribute:value} #'ReceiveMessageWaitTimeSeconds': '20'
    )
# List all queues
def get_all_queues():
    response = sqs.list_queues()
    return response['QueueUrls']

# Get queue url given queue name
def get_queue_url(q_name):
    response = sqs.get_queue_url(QueueName=q_name)
    return response['QueueUrl']

# Delete a queue given queue name
def delete_queue(q_name):
    q_url = get_queue_url(q_name)
    if q_url is not None:
        sqs.delete_queue(QueueUrl=q_url)

def send_msg(q_name, msg_attribs, msg_body):
    """
    sample_msg_attrib = {
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        }
    sample_msg_body = 'Information about current NY Times fiction bestseller for week of 12/11/2016.'
    """
    # Get queue url
    queue_url = get_queue_url(q_name)
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageAttributes= msg_attribs,
        MessageBody=msg_body,
        MessageGroupId='1'
    )

    return response['MessageId']

def receive_msg(q_name):
    # Get queue url
    queue_url = get_queue_url(q_name)
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=60,
        WaitTimeSeconds=20
    )
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    return message, receipt_handle

def delete_msg(q_name, message, receipt_handle):
    # Get queue url
    queue_url = get_queue_url(q_name)
    # message, receipt_handle = receive_msg(q_name)
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Deleted received message: %s' % message)
    return message


def get_msg_count(q_name):
    response = sqs.get_queue_attributes(
        QueueUrl=get_queue_url(q_name),
        AttributeNames=[
            'ApproximateNumberOfMessages'
        ]
    )
    return response['Attributes']['ApproximateNumberOfMessages']

if __name__ == "__main__":
    # create_queue(const.ANALYSIS_QUEUE, fifo=True)
    # update_queue(const.UPLOAD_QUEUE, 'ReceiveMessageWaitTimeSeconds', '20')
    # delete_queue('content-upload-q')
    # qs = get_all_queues()
    # for q in qs:
    #     print(q)

    # push 10 dummy messages to queue
    for i in range(10):
        message_attrib = {
                str(time.clock()) : {
                    'DataType': 'String',
                    'StringValue': str(i)
                }
            }
        msg_body = 'This is message '+str(i)
        print(send_msg(const.ANALYSIS_QUEUE, message_attrib, msg_body))
        print()