#!/usr/bin/python

import boto3
import queue_util as queue_util
import s3_util as s3_util
import subprocess
import psutil
from global_constants import GlobalConstants
import parse
import os
import time
import ec2_util as ec2_util
from ec2_metadata import ec2_metadata
import sys
# import requests
const = GlobalConstants()

processed_dir = os.path.expanduser(os.path.join('~','pi-eye-py','ec2_results'))
print("result dir:" +processed_dir)
queue_url = queue_util.get_queue_url(const.ANALYSIS_QUEUE)
if not os.path.isdir(processed_dir):
  os.mkdir(processed_dir)

vid_dir = os.path.expanduser(os.path.join('~','pi-eye-py','ec2_videos'))
print("vid dir:" + vid_dir)
if not os.path.isdir(vid_dir):
  os.mkdir(vid_dir)

# /home/shantanu/Desktop/repos/darknet

def analyze_ec2(filename):
    start = time.time()
    # download video file to vid_dir
    s3_util.download_video(filename, vid_dir)
    print("time to download {} is {}".format(filename,time.time()-start))
    abs_path = os.path.join(vid_dir,filename)
    #print("filename: " + filename)
    #print("abs_path: " + abs_path)
    print("current file being processed is : " + filename)
    os.chdir(os.path.expanduser("~/darknet"))
    com = "Xvfb :1 & export DISPLAY=:1"
    proc = subprocess.Popen([com], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    command = "./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights {0}".format(abs_path)
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("time to analyze video {} is {}".format(filename,time.time()-start))
    result_value = parse.parse_result(out)
    #move from /ec2_videos to /ec2_results
    try:
      # subprocess.run((' ').join(['mv',abs_path,processed_dir]),shell=True, check=True)
      subprocess.run((' ').join(['rm', '-rf', abs_path]),shell=True, check=True)
    except:
      print("Unexpected error while moving file: " + str(sys.exc_info()[0]))
    return result_value

if __name__ == '__main__':

    while(1):
        if (psutil.cpu_percent() <= 85):
            try:
              filename, receipt_handle = queue_util.receive_msg(queue_url)
              print('Received file ',filename)
            except:
              print("Unexpected error while receiving message: " + str(sys.exc_info()[0]))
              continue
              # raise

            if filename is not None:
                result_value = analyze_ec2(os.path.basename(filename))
                try:
                  print('done processing.... detected: %s\n' %result_value)
                  s3_util.upload_results(filename,result_value)
                  queue_util.delete_msg(queue_url,filename,receipt_handle)
                except:
                  print("Unexpected error while deleting message: " + str(sys.exc_info()[0]))
                  raise
            else:
                # stop logic
                instance_id = ec2_metadata.instance_id
                # alternative logic
                # count = 0
                # instance_id = ''
                # while instance_id == '':
                #   try:
                #     r = requests.get("http://169.254.169.254/latest/dynamic/instance-identity/document")
                #     response_json = r.json()
                #     region = response_json.get('region')
                #     instance_id = response_json.get('instanceId')
                #   except:
                #     count +=1
                # print('No pending request, shutting down... on count ',count)
                if instance_id != '': 
                  print('No pending request, shutting down...')
                  ec2_util.stop_instances([instance_id])
                  break
        else:
            pass
