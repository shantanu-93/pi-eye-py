import os
import sys
from datetime import datetime
import subprocess
import boto3
from global_constants import GlobalConstants
from queues import *
from find_most_recent import allFilesIn
from time import sleep


global_const = GlobalConstants()

def create_q():
    # create analysis queue
    analysis_queue = create_queue(global_const.ANALYSIS_QUEUE)
    queue_url =get_queue_url(global_const.ANALYSIS_QUEUE)

if __name__ == '__main__':

    create_q()

    if(os.path.exists('.\\analysis_queue_videos')):
        print("Directory already exits!")
    else:
        subprocess.call(['mkdir','analysis_queue_videos'])

    os.chdir(".\\record_videos")

    try:
        while True:

            # code to find the latest file
            latest_subdir = max(allFilesIn('.'), key=os.path.getmtime)
            print(latest_subdir)
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

            MessageBody=(
                    'testing hahaha'
                )
            ret = send_msg(global_const.ANALYSIS_QUEUE,MessageAttributes,MessageBody)

            subprocess.call(['mv',latest_subdir,'..\\analysis_queue_videos'])

            if not os.listdir('.'):
                print("Directory is empty!")
            else:
                continue

            sleep(3600)



    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error: " + str(sys.exc_info()[0]))
        raise