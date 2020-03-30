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
from math import ceil,floor
from botocore.exceptions import ClientError

const = GlobalConstants()

sqs = boto3.client('sqs')
''', region_name=const.REGION,
    aws_access_key_id=const.ACCESS_KEY,
    aws_secret_access_key=const.SECRET_KEY)'''
queue_url = queue_util.get_queue_url(const.ANALYSIS_QUEUE)
recording_vids = os.path.expanduser('~/pi-eye-py/record_videos/*.h264')
pi_vids = os.path.expanduser('~/pi-eye-py/pi_videos/*.h264')

def get_file_numbers(dir):
    return len(os.listdir(dir))

def distribute_work_pi_ec2(pi_video_count, new_video_count):
    # if pending on pi  less than threshold, assign difference with threshold to pi rest ec2
    pending_msg_count = int(queue_util.get_msg_count(queue_url))

    # total_videos = pi_video_count+new_video_count+pending_msg_count
    assign_pi = 0 #int((const.MIN_NO_AXN*new_video_count)//(const.MAX_WORKERS + const.MIN_NO_AXN)) - pi_video_count
    assign_ec2 = 0  # total_videos - assign_pi
    
    # if pi_video_count+new_video_count <= const.MIN_NO_AXN:
    #     return new_video_count, 0
    # else:
    #     if pending_msg_count > const.MAX_WORKERS - const.MIN_NO_AXN:
    #         # say there are 23 new vids, pi threshold(4) and max(19) ec2 workers are running, divide 4:19
    #         distribute_load = floor((new_video_count)/const.MIN_NO_AXN)-1
    #         # distribute_load = int((const.MIN_NO_AXN*new_video_count)//(const.MAX_WORKERS + const.MIN_NO_AXN))
    #         print("Pi {} EC2 {}".format(distribute_load, new_video_count-distribute_load))
    #         return distribute_load, new_video_count-distribute_load
    #     else:
    #         assign_pi = const.MIN_NO_AXN - pi_video_count
    #         return assign_pi, new_video_count-assign_pi
    
    while new_video_count>0:
        if pi_video_count+assign_pi < const.MIN_NO_AXN:
            # assign for pi less than threshold
            temp = min(new_video_count, const.MIN_NO_AXN - pi_video_count)
            new_video_count -= temp
            assign_pi += temp
        else:
            if pending_msg_count+assign_ec2< const.MAX_WORKERS:
                # assign for new ec2
                temp = min(new_video_count, const.MAX_WORKERS - pending_msg_count)
                new_video_count -= temp
                assign_ec2 += temp
                # assign for value of threshold
            else:
                if ((pending_msg_count+assign_ec2)*const.MIN_NO_AXN)<((pi_video_count+assign_pi)*const.MAX_WORKERS):
                    temp = min(const.MAX_WORKERS,new_video_count)
                    new_video_count -= temp
                    assign_ec2 += temp
                else:
                    temp = min(const.MIN_NO_AXN,new_video_count)
                    new_video_count -= temp
                    assign_pi+=temp

                # assign one each for all ec2 instances
                # if new_video_count>0:
                #     temp += min(const.MAX_WORKERS,new_video_count)
                #     new_video_count -= temp
                #     assign_ec2 +=temp
    print("\nCurrent: Pi {} EC2 {}".format(pi_video_count,pending_msg_count))
    print("\nNew: Pi {} EC2 {}\n".format(pi_video_count+assign_pi,pending_msg_count+assign_ec2))
    return assign_pi,assign_ec2

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

            if len(list_of_files)>0:
                pi_video_count = len(glob.glob(pi_vids))
                new_video_count = len(list_of_files)
                pi,ec2 = distribute_work_pi_ec2(pi_video_count, new_video_count)
                print("Pi count {} EC2 count {}".format(pi, ec2))
                # move videos to /pi_videos
                moved_to_pi = []
                for _ in range(pi):
                    latest_subdir = os.path.abspath(min(glob.glob(recording_vids), key=os.path.getmtime))
                    moved_to_pi.append(latest_subdir)
                    # print(latest_subdir)
                    subprocess.run((' ').join(['mv',latest_subdir,os.path.expanduser('~/pi-eye-py/pi_videos/')]),shell=True, check=True)
                print("\n Time taken to move to pi videos: ",time.time()-start)
                # upload videos to s3
                if ec2 > 0:
                    move_to_ec2 = glob.glob(recording_vids) #list(set(list_of_files) - set(moved_to_pi)) #
                    try:
                        s3_util.upload_videos(move_to_ec2)
                    except ClientError:
                        print("Files to upload %s" %move_to_ec2)
                        print("Botocore error: " + str(sys.exc_info()[0]))
                        continue
                    except:
                        print("Unexpected error: " + str(sys.exc_info()[0]))
                        continue
                    print("\n Time taken to upload to s3 {}, count {}".format(time.time()-start, len(move_to_ec2)))

                    # move videos to /analysis_queue_videos and push to sqs
                    sent_to_ec2 = []
                    for _ in range(ec2):
                        vids = list(set(move_to_ec2) - set(sent_to_ec2))
                        if len(vids)>0:
                            latest_subdir = min(vids, key=os.path.getmtime)
                            sent_to_ec2.append(latest_subdir)
                            # print(latest_subdir)
                            MessageBody=os.path.basename(latest_subdir)
                            ret = sqs.send_message(QueueUrl=queue_url,MessageBody=MessageBody,MessageGroupId='msggpid1')
                            print(latest_subdir," sent to queue!")
                            subprocess.run((' ').join(['mv',latest_subdir,os.path.expanduser('~/pi-eye-py/analysis_queue_videos')]),shell=True, check=True)
                        else:
                            break
                    print("\n Time taken to send to sqs {}, count {}".format(time.time()-start, len(move_to_ec2)))

            else:
                # TODO: See if required
                time.sleep(5)
            print("\nPolling recording directory")

    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error: " + str(sys.exc_info()[0]))
        raise
