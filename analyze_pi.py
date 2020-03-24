#!/usr/bin/python
import os
import subprocess
import queue_util as queue_util
from global_constants import GlobalConstants
# from find_most_recent import allFilesIn
import sys

#subprocess.call(['./darknet','detector','demo','cfg/coco.data','cfg/yolov3-tiny.cfg','yolov3-tiny.weights','../facedetect/record_videos/2020-03-14_15.45.33.h264'])

#os.chdir("/home/pi/facedetect/record_videos")
const = GlobalConstants()
message , receipt = queue_util.receive_msg(const.ANALYSIS_QUEUE_URL)


if __name__ == '__main__':

    os.chdir("~/darknet")

    try:
        while True:
            while os.listdir('./pi_videos'):
                latest_subdir = max(os.listdir(), key=os.path.getmtime)
                result = latest_subdir[:-5] + '_result.txt'
                subprocess.call(['./darknet','detector','demo','cfg/coco.data','cfg/yolov3-tiny.cfg','yolov3-tiny.weights',latest_subdir,'>',result])
                subprocess.call(['rm',latest_subdir])

    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error:" + str(sys.exc_info()[0]))
        raise