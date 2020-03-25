#!/usr/bin/python

'''
SETUP:

    -   -->     GND     -->     PIN14
    +   -->     5V      -->     PIN2
    S   -->     GPIO18  -->     PIN12

'''

import RPi.GPIO as GPIO
import subprocess
import time
import sys

sensor = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)

on = 0
off = 0
flag = 0
while flag == 0:
    i=GPIO.input(sensor)
    if i == 0:
        if flag == 1:
            off = time.time()
            diff = off - on
            print 'time: ' + str(diff%60) + ' sec'
            print ''
            flag = 0
        print "No intruders"
        print 'i: ' + str(i)
        print 'flag: ' + str(flag)
        time.sleep(1)
    elif i == 1:
        if flag == 0:
            print "Intruder detected"
            on = time.time()
            #flag = 1
            #subprocess.call(['python','take_snapshot.py','frame.jpg'])
            subprocess.call(['python','record.py'])
            #subprocess.call(['./facedetect', 'frame.jpg'])
        print 'i: ' + str(i)
        print 'flag: ' + str(flag)
        time.sleep(0.1)
