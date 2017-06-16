#!/usr/bin/env python2

import RFM69
from RFM69registers import *
import datetime
import time

NODE=1
NET=1
KEY="Something16chars"
TIMEOUT=3
TOSLEEP=0.1

radio = RFM69.RFM69(RF69_915MHZ, NODE, NET, True)
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
    
# Need an if then loop here for MPC control? Or just play/pause music if data = Pressed (2 sec debounce on the other end)... Propbably MPC/MPD I think
# Loop should react to data being "Pressed", then reset data to an empty string and sleep for 2 sec.

print "shutting down"
radio.shutdown()
