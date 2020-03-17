#!/usr/bin/python
import os
import subprocess
import glob
os.chdir("/home/pi/darknet")
#subprocess.call(['./darknet','detector','demo','cfg/coco.data','cfg/yolov3-tiny.cfg','yolov3-tiny.weights','../facedetect/record_videos/2020-03-14_15.45.33.h264'])

#os.chdir("/home/pi/facedetect/record_videos")
for infile in sorted(glob.glob('/home/pi/facedetect/record_videos/*.h264')):
    print "current file being processed is :" + infile
    subprocess.call(['./darknet','detector','demo','cfg/coco.data','cfg/yolov3-tiny.cfg','yolov3-tiny.weights',infile])
