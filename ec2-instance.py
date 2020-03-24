import queue_util as queue_util
import s3_util as s3_util
import subprocess
import psutil
from global_constants import GlobalConstants
import os
import time as time
import ec2_util as ec2_util
from ec2_metadata import ec2_metadata

const = GlobalConstants()
vid_dir = os.path.expanduser(os.path.join('~','analyze_videos'))
if not os.path.isdir(vid_dir):
    os.mkdir(vid_dir)

# /home/shantanu/Desktop/repos/darknet

def analyze_ec2(filename): # const.VIDEO_BUCKET, filename, os.path.join(target_dir,filename)
    # download video file to dir
    s3_util.download_video(filename, vid_dir)
    abs_path = os.path.join(vid_dir,filename)
    print("current file being processed is : " + filename)
    os.chdir(os.path.expanduser("~/darknet"))
    result = subprocess.check_output(['./darknet','detector','demo','cfg/coco.data','cfg/yolov3-tiny.cfg','yolov3-tiny.weights',abs_path])
    result_file = result ## TODO: call parse result method here to store result in file
    s3_util.upload_results([result_file])

while(1):
    if (psutil.cpu_percent() <= 85):
        filename, receipt_handle = queue_util.receive_msg(const.ANALYSIS_QUEUE_URL)
        if filename is not None:
            analyze_ec2(filename)
            queue_util.delete_msg(const.ANALYSIS_QUEUE_URL,filename,receipt_handle)
        else:
            # stop logic
            instance_id = ec2_metadata.instance_id # urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
            ec2_util.stop_instances([instance_id])
    else:
        pass




