# import boto3
# client = boto3.client('sqs',region_name='us-east-1')
# print('Creating a fifo queue')
# client.create_queue(QueueName='my_fifo_queue.fifo', Attributes={'FifoQueue': 'true','ContentBasedDeduplication': 'true'})
# queues = client.list_queues(QueueNamePrefix='my_fifo_queue')
# queue_url = queues['QueueUrls'][0]
# print('Sending 10 messages to the fifo queue')
# for i in range(0,10):
#     print('message: '+ str(i))
#     enqueue_response = client.send_message(QueueUrl=queue_url, MessageBody='message: '+str(i), MessageGroupId='msggpid1')
# print('Receving 20 messages from the fifo queue')
# while True:
#     messages = client.receive_message(QueueUrl=queue_url,MaxNumberOfMessages=5)
#     if 'Messages' in messages:
#         for message in messages['Messages']:
#             print(message['Body'])
#             # client.delete_message(QueueUrl=queue_url,ReceiptHandle=message['ReceiptHandle'])
#     else:
#         print('Queue is now empty')
#         break
# client.delete_queue(QueueUrl=queue_url)
# print('Queue is now deleted')

if __name__ == '__main__':
    with open('123.txt','w') as f:
        f.write('hello')

