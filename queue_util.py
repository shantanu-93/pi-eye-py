import boto3
from global_constants import GlobalConstants
import time
const = GlobalConstants()

# SQS client
# max_queue_messages = 10
# message_bodies = []
sqs = boto3.client('sqs')
''', region_name=GlobalConstants().REGION,
        aws_access_key_id=GlobalConstants().ACCESS_KEY,
        aws_secret_access_key=GlobalConstants().SECRET_KEY)'''


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

def update_queue(queue_url, attribute, value):
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
def delete_queue(q_url):
    if q_url is not None:
        sqs.delete_queue(QueueUrl=q_url)

def send_msg(queue_url, msg_attribs, msg_body):
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
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=0,
        MessageAttributes=msg_attribs,
        MessageBody=msg_body,
        MessageGroupId='1'
    )

    return response['MessageId']

def receive_msg(queue_url):
    # Get queue url
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=120,
        WaitTimeSeconds=20
    )
    # if response in not None
    if 'Messages' in response:
        message = response['Messages'][0]['Body']
        receipt_handle = response['Messages'][0]['ReceiptHandle']
    else:
        return None,None
    return message, receipt_handle

def delete_msg(queue_url, message, receipt_handle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Deleted received message: %s' % message)
    return message


def get_msg_count(queue_url):
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
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
    #send_msg(get_queue_url(const.ANALYSIS_QUEUE),"test", {})
    pass