import boto3

# SQS client
sqs = boto3.client('sqs')

# Create a queue
def create_queue(q_name, delay_sec = None, retention_pd = None):
    response = sqs.create_queue(
        QueueName=q_name,
        Attributes={
            'DelaySeconds': '60' if delay_sec is None else str(delay_sec),
            'MessageRetentionPeriod': '86400' if retention_pd is None else str(retention_pd) #
        }
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
        DelaySeconds=10,
        MessageAttributes= msg_attribs,
        MessageBody=(msg_body)
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
        VisibilityTimeout=0,
        WaitTimeSeconds=0
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


