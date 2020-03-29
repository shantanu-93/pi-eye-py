import os
import sys
from datetime import datetime
import subprocess
import boto3
import glob
from global_constants import GlobalConstants
import queue_util as queue_util
import s3_util as s3_util
# from find_most_recent import allFilesIn
import time

const = GlobalConstants()

sqs = boto3.client('sqs')
''', region_name=const.REGION,
    aws_access_key_id=const.ACCESS_KEY,
    aws_secret_access_key=const.SECRET_KEY)'''
queue_url = queue_util.get_queue_url(const.ANALYSIS_QUEUE)
recording_vids = os.path.expanduser('~/pi-eye-py/record_videos/*.h264')

def get_file_numbers(dir):
    return len(os.listdir(dir))

def controller(number):
    if number <= 2:
        return number,0
    else:
        return int(number/3), number-int(number/3)


if __name__ == '__main__':

    if not os.path.exists('analysis_queue_videos'):
    #     print("/analysis_queue_videos!")
    # else:
        subprocess.call(['mkdir','analysis_queue_videos'])
    if not os.path.exists('pi_videos'):
    #     print("/pi_videos already exits!")
    # else:
        subprocess.call(['mkdir','pi_videos'])

    record_dir = os.path.expanduser("~/pi-eye-py/record_videos")
    if not os.path.exists(record_dir):
        subprocess.call(['mkdir',record_dir])
    os.chdir(record_dir)
    try:
        while True:

            # assign videos to pi and ec2
            start = time.time()
            list_of_files = glob.glob(recording_vids)

            file_number = len(list_of_files)
            pi,ec2 = controller(file_number)
            print("Pi count {} EC2 count {}".format(pi, ec2))

            if len(list_of_files)>0:
                # move videos to /pi_videos
                for _ in range(pi):
                    latest_subdir = os.path.abspath(min(list_of_files, key=os.path.getmtime))
                    # print(latest_subdir)
                    subprocess.run((' ').join(['mv',latest_subdir,os.path.expanduser('~/pi-eye-py/pi_videos/')]),shell=True, check=True)
                print("\n Time taken to move to pi videos: ",time.time()-start)
                # upload videos to s3
                if ec2 > 0:
                    ec2_vid = glob.glob(recording_vids)
                    s3_util.upload_videos(ec2_vid)
                    print("\n Time taken to upload to s3 {}, count {}".format(time.time()-start, len(ec2_vid)))

                    # move videos to /analysis_queue_videos and push to sqs
                    for _ in range(ec2):
                        latest_subdir = min(glob.glob(recording_vids), key=os.path.getmtime)
                        # print(latest_subdir)
                        MessageBody=str(latest_subdir)
                        ret = sqs.send_message(QueueUrl=queue_url,MessageBody=MessageBody,MessageGroupId='msggpid1')
                        print(latest_subdir," sent to queue!")
                        subprocess.run((' ').join(['mv',latest_subdir,os.path.expanduser('~/pi-eye-py/analysis_queue_videos')]),shell=True, check=True)
                    print("\n Time taken to send to sqs {}, count {}".format(time.time()-start, len(ec2_vid)))

            else:
                # TODO: See if required
                time.sleep(5)
            print("\nPolling recording directory")

    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error: " + str(sys.exc_info()[0]))
        raise
