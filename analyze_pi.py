#!/usr/bin/python
import os
import subprocess
import glob
import queue_util as queue_util
from global_constants import GlobalConstants
# from find_most_recent import allFilesIn
import sys

#subprocess.call(['./darknet','detector','demo','cfg/coco.data','cfg/yolov3-tiny.cfg','yolov3-tiny.weights','../facedetect/record_videos/2020-03-14_15.45.33.h264'])

#os.chdir("/home/pi/facedetect/record_videos")
const = GlobalConstants()
#message , receipt = queue_util.receive_msg(queue_util.get_queue_url(const.ANALYSIS_QUEUE))
analysis_dir = "/home/pi/pi-eye-py/pi_videos/"
result_dir = "/home/pi/pi-eye-py/pi_results/"
processed_dir = "/home/pi/pi-eye-py/processed_videos/"


if __name__ == '__main__':

    os.chdir("/home/pi/darknet")

    try:
        while True:
            # list_of_files = glob.glob('/home/pi/pi-eye-py/pi_videos/*')
            # print("list_of_files: ",list_of_files)
            while os.listdir(analysis_dir):
                list_of_files = glob.glob(analysis_dir+'/*')
                print("list_of_files: ",list_of_files)
                latest_subdir = os.path.abspath(min(list_of_files, key=os.path.getmtime))
                print("Video File: ",latest_subdir)
                result_file = os.path.join(result_dir,str(os.path.basename(latest_subdir)[:-5] + '_result.txt'))
                print("Result File: ",result_file)
                command = "./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights {0}".format(latest_subdir)
                proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		with open(result_file, 'w') as fout:
                	fout.write(out)
                os.system('mv {0} {1}'.format(latest_subdir,processed_dir))
                # TODO: remove above uncomment below
                # os.system('rm -rf %s' %latest_subdir)
             
    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error:" + str(sys.exc_info()[0]))
        raise
