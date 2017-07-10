#!/usr/bin/env python2

import RFM69
from RFM69registers import *
import datetime
import time
import subprocess
import os
#import sys

NODE=1
NET=1
KEY="Something16Chars"
TIMEOUT=3
TOSLEEP=0.1
playerprocess = None
soundfile1 = "/home/pi/bubblebutt.mp3"

def playSound(soundFile):
    # check that we have started a process and the process is still running
    global playerprocess
    print playerprocess
    if (playerprocess != None): # and (playerprocess.poll()):
        # Dirty way to end it I guess because subprocess got updated in Python3 and is a bitch now.
        os.system("pkill -9 mpg321")
        playerprocess = None
    else:
        # start new process
        playerprocess = subprocess.Popen('mpg321 ' + soundFile , shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

radio = RFM69.RFM69(RF69_433MHZ, NODE, NET, True)
print "class initialized"

print "reading all registers"
results = radio.readAllRegs()
#for result in results:
#    print result

print "Performing rcCalibration"
radio.rcCalibration()

print "setting high power"
radio.setHighPower(True)

print "Checking temperature"
print radio.readTemperature(0)

print "setting encryption"
radio.encrypt(KEY)

print "starting loop..."
sequence = 0
while True:

    data=None
    print "start recv..."
    radio.receiveBegin()
    timedOut=0
    while not radio.receiveDone():
        timedOut+=TOSLEEP
        time.sleep(TOSLEEP)
        if timedOut > TIMEOUT:
            print "timed out waiting for recv"
            break
    if radio.ACKRequested():
        print "sending ack..."
        radio.sendACK()
    else:
        print "ack not requested..."
    print "end recv..."
    data = "".join([chr(letter) for letter in radio.DATA])
    print data
    if data == 'Pressed':
        print "Button pressed! data is "+data
	playSound(soundfile1)
#        if (playerprocess != None) and (playerprocess.poll()):
#            playerprocess.stdin.close()
#            playerprocess.terminate()
#        else:# start new process
#            playerprocess = subprocess.Popen('mpg321 ' + soundfile1 , stdout=subprocess.PIPE, shell=True)
#            #playerprocess.stdout.close()
##            playerprocess.wait()
        radio.DATA = []

# Need an if then loop here for MPC control? Or just play/pause music if data = Pressed (2 sec debounce on the other end)... Propbably MPC/MPD I think
# Loop should react to data being "Pressed", then reset data to an empty string and sleep for 2 sec.



print "shutting down"
radio.shutdown()

