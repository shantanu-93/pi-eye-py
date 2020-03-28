from picamera import PiCamera
import time
import datetime
import os

camera = PiCamera()
os.chdir("./record_videos")
#function to create new filename from date and time
def getFileName():
   return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

filename = getFileName()
camera.start_preview()
camera.start_recording(filename)
camera.wait_recording(10)
camera.stop_preview()
camera.stop_recording()

