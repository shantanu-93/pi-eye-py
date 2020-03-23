import queue_util as q
import s3_util as s3
import glob
import subprocess
import psutil
import threading

queue_url = 'https://queue.amazonaws.com/952986094592/video-analysis-q.fifo'





def analyze_ec2(message):
    s3.download_video(message, '')
    for infile in sorted(glob.glob('record.h264')):
        print("current file being processed is :" + infile)
        result = subprocess.check_output(['./darknet','detector','demo','cfg/coco.data','cfg/yolov3-tiny.cfg','yolov3-tiny.weights',infile])
        filter(result)
        s3.upload_results(result)


def filter(result):
    pass


while(1):
    if (psutil.cpu_percent() <= 85):
        message = q.receive_msg(queue_url)
        q.delete_msg(queue_url,message,"deleting the msg")
        message = "record.h264"
        analyze_ec2(message)
        # t = threading.Thread(target=python_cli_command_dump_s3())
        # t.start()
        # threads.append(t)
        # threads = [t for t in threads if t.isAlive()]

    else:
        pass




