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

const = GlobalConstants()
analysis_dir = "/home/pi/pi-eye-py/pi_videos/"
result_dir = "/home/pi/pi-eye-py/pi_results/"
processed_dir = "/home/pi/pi-eye-py/processed_videos/"


if __name__ == '__main__':

    os.chdir("/home/pi/darknet")

    try:
        while True:
            if (psutil.cpu_percent() <= 85):
                while os.listdir(analysis_dir):
                    list_of_files = glob.glob(analysis_dir+'/*')
                    print("list_of_files: ",list_of_files)
                    latest_subdir = os.path.abspath(min(list_of_files, key=os.path.getmtime))
                    print("Video File: ",latest_subdir)
                    result_file = os.path.join(result_dir,str(os.path.basename(latest_subdir)[:-5] + '_result.txt'))
                    print("Result File: ",result_file)
                    output_file = result_file.replace('_result','_output')
                    command = "./darknet detector demo cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights {0}".format(latest_subdir)
                    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
                    (out, err) = proc.communicate()
                    with open(result_file, 'w') as fout:
                        fout.write(out)
                    with open(output_file, 'w') as fout:
                        fout.write(parse.parse_result(output_file))
                    if output_file is not None:
                        s3_util.upload_results([output_file])
                    os.system('mv {0} {1}'.format(latest_subdir,processed_dir))
                    # TODO: comment above uncomment below
                    # os.system('rm -rf %s' %latest_subdir)
             
    except KeyboardInterrupt:
        print("Quitting the program.")
    except:
        print("Unexpected error:" + str(sys.exc_info()[0]))
        raise
