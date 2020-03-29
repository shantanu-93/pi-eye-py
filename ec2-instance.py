#!/usr/bin/python

import queue_util as queue_util
import s3_util as s3_util
import subprocess
import psutil
from global_constants import GlobalConstants
import parse
import os
import time as time
import ec2_util as ec2_util
from ec2_metadata import ec2_metadata

const = GlobalConstants()

result_dir = os.path.expanduser(os.path.join('~','pi-eye-py','ec2_results'))
print("result dir:" +result_dir)
if not os.path.isdir(result_dir):
  os.mkdir(result_dir)
  
vid_dir = os.path.expanduser(os.path.join('~','pi-eye-py','ec2_videos'))
print("vid dir:" + vid_dir)
if not os.path.isdir(vid_dir):
  os.mkdir(vid_dir)

# /home/shantanu/Desktop/repos/darknet

def analyze_ec2(filename): # const.VIDEO_BUCKET, filename, os.path.join(target_dir,filename)
    # download video file to dir
    s3_util.download_video(filename, vid_dir)
    abs_path = os.path.join(vid_dir,filename)
    #print("abs_path:" + abs_path)
    print("current file being processed is : " + filename)
    result_file = abs_path[:-5] + '_result.txt'
    #print("result file:" + result_file)
    os.chdir(os.path.expanduser("~/darknet"))
    output_file = result_file.replace('_result','_output')
    #print("output file:" + output_file)
    command = "./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights {0}".format(abs_path)
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    with open(result_file, 'w') as fout:
      fout.write(str(out))
    with open(output_file, 'w') as fout:
      fout.write(str(parse.parse_result(result_file)))
    
    
    s3_util.upload_results(['test'])
    #move from /ec2_videos to /ec2_results
    os.system('mv {0} {1}'.format(output_file,result_dir))
    #remove

if __name__ == '__main__':
    
    while(1):
        if (psutil.cpu_percent() <= 85):
            filename, receipt_handle = queue_util.receive_msg(queue_util.get_queue_url(const.ANALYSIS_QUEUE))
            if filename is not None:
                analyze_ec2(filename)
                #queue_util.delete_msg(queue_util.get_queue_url(const.ANALYSIS_QUEUE),filename,receipt_handle)
		            print('done processing....\n')
            else:
                # stop logic
                instance_id = ec2_metadata.instance_id # urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read().decode()
                print('no pending request, shutting down...\n')
                ec2_util.stop_instances([instance_id])
        else:
            pass
