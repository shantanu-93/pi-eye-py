#!/usr/bin/python
import os
import subprocess
import glob
import queue_util
from global_constants import GlobalConstants
import sys
import psutil
import s3_util
import parse
import time

const = GlobalConstants()
analysis_dir = os.path.expanduser("~/pi-eye-py/pi_videos/")
result_dir = os.path.expanduser("~/pi-eye-py/pi_results/")
processed_dir = os.path.expanduser("~/pi-eye-py/processed_videos/")


if __name__ == '__main__':

    os.chdir(os.path.expanduser("~/darknet"))

    try:
        while True:
            if (psutil.cpu_percent(interval=1) <= 85):
                if os.listdir(analysis_dir):
                    start = time.time()
                    list_of_files = glob.glob(analysis_dir+'/*.h264')
                    print("list_of_files: ",list_of_files)
                    latest_subdir = os.path.abspath(min(list_of_files, key=os.path.getmtime))
                    filename = (os.path.basename(latest_subdir))
                    print("Processing Video File: ",latest_subdir)
                    command = "./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights {0}".format(latest_subdir)
                    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
                    (out, err) = proc.communicate()
                    print("\n Time taken to analyze video {} is {} ".format(filename,time.time()-start))

                    # result_file = os.path.join(result_dir,str(os.path.basename(latest_subdir)[:-5] + '_result.txt'))
                    # with open(result_file, 'w') as fout:
                    #     fout.write(str(parse.parse_result(str(out))))
                    # output_file = result_file.replace('_result','_output')
                    # with open(output_file, 'w') as fout:
                    #     fout.write(str(out))
                    result_key = str(filename[:-5] + '_result.txt')
                    print("Uploading Result File: ",result_key)
                    s3_util.upload_results(result_key,parse.parse_result(str(out)))
                    subprocess.run('mv {0} {1}'.format(latest_subdir,processed_dir),shell=True, check=True)
                    # TODO: comment above uncomment below
                    # os.system('rm -rf %s' %latest_subdir)
                else:
                    time.sleep(2)
                print("Polling pi_videos directory")
             
    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error:" + str(sys.exc_info()[0]))
        raise
