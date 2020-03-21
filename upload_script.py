import os
import sys
from datetime import datetime
import subprocess
import boto3
from global_constants import GlobalConstants
import queue_util as queue_util
import s3_util as s3_util
from find_most_recent import allFilesIn
from time import sleep

const = GlobalConstants()

# def create_q():
    # create analysis queue
    # analysis_queue = create_queue(global_const.ANALYSIS_QUEUE, fifo=True)
    # queue_url = get_queue_url(global_const.ANALYSIS_QUEUE)

def get_file_numbers(dir):
    return len(os.listdir(dir))

def controller(number):
    if number <= 2:
        return number,0
    else:
        return int(number/3), number-int(number/3)




if __name__ == '__main__':

    sqs = boto3.client('sqs',region_name='us-east-1')
    sqs.create_queue(QueueName=const.ANALYSIS_QUEUE,Attributes={'FifoQueue': 'true','ContentBasedDeduplication': 'true'})
    queues = sqs.list_queues(QueueNamePrefix=const.ANALYSIS_QUEUE)
    queue_url = queues['QueueUrls'][0]
    # print(queue_url)

    if(os.path.exists('analysis_queue_videos')):
        print("/analysis_queue_videos!")
    elif(os.path.exists('pi_videos')):
        print("/pi_videos already exits!")
    else:
        subprocess.call(['mkdir','analysis_queue_videos'])
        subprocess.call(['mkdir','pi_videos'])

    os.chdir("record_videos")

    try:
        while True:

            # assign videos to pi and ec2
            file_number = get_file_numbers('.')
            pi,ec2 = controller(file_number)
            print(pi,ec2)

            # upload videos to s3
            for files in os.listdir('.'):
                s3_util.upload_videos([os.path.join(os.getcwd(), files)])

            # move videos to /pi_videos
            for _ in range(pi):
                latest_subdir = max(os.listdir(), key=os.path.getmtime)
                # print(latest_subdir)
                subprocess.call(['mv',latest_subdir,'..\\pi_videos'])

            # move videos to /analysis_queue_videos and push to sqs
            for _ in range(ec2):
                latest_subdir = max(os.listdir(), key=os.path.getmtime)
                # print(latest_subdir)
                MessageBody=str(latest_subdir)
                ret = sqs.send_message(QueueUrl=queue_url,MessageBody=MessageBody,MessageGroupId='msggpid1')

                subprocess.call(['mv',latest_subdir,'..\\analysis_queue_videos'])

            # polling /record_videos and check if it's empty
            if not os.listdir('.'):
                print("Directory is empty!")

            sleep(60)



    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error: " + str(sys.exc_info()[0]))
        raise