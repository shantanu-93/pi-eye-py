import os
import sys
from datetime import datetime
import subprocess
import boto3
from global_constants import GlobalConstants
from queue_util import *
import s3_util as s3_util
from find_most_recent import allFilesIn
from time import sleep



# def create_q():
    # create analysis queue
    # analysis_queue = create_queue(global_const.ANALYSIS_QUEUE, fifo=True)
    # queue_url = get_queue_url(global_const.ANALYSIS_QUEUE)

if __name__ == '__main__':

    sqs = boto3.client('sqs',region_name='us-east-1')
    sqs.create_queue(QueueName=GlobalConstants().ANALYSIS_QUEUE,Attributes={'FifoQueue': 'true','ContentBasedDeduplication': 'true'})
    queues = sqs.list_queues(QueueNamePrefix=GlobalConstants().ANALYSIS_QUEUE)
    queue_url = queues['QueueUrls'][0]
    # print(queue_url)

    if(os.path.exists('analysis_queue_videos')):
        print("Directory already exits!")
    else:
        subprocess.call(['mkdir','analysis_queue_videos'])

    os.chdir("record_videos")

    try:
        while True:

            # code to find the latest file
            latest_subdir = max(os.listdir(), key=os.path.getmtime)
            print(latest_subdir)
            print(os.path.join(os.getcwd(), latest_subdir))
            # s3_util.upload_videos(os.path.join(os.getcwd(), latest_subdir))

            # code to move to /analysis_queue_videos and push into analysis queue

            MessageAttributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': str(latest_subdir)
                },
                'Status': {
                    'DataType': 'String',
                    'StringValue': 'idle'
                }
            }

            MessageBody='testing hahaha'
            ret = sqs.send_message(QueueUrl=queue_url,MessageBody=MessageBody,MessageAttributes=MessageAttributes,MessageGroupId='msggpid1')

            subprocess.call(['mv',latest_subdir,'..\\analysis_queue_videos'])

            if not os.listdir('.'):
                print("Directory is empty!")
                break
            else:
                continue

            sleep(3600)



    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error: " + str(sys.exc_info()[0]))
        raise