#!/usr/bin/env python2

import RFM69
from RFM69registers import *
import datetime
import time
import RPi.GPIO as GPIO

#Set pin and node!
pin=12
ledpin=11
NODE=2
NET=1
KEY="Something16Chars"
msg = "Pressed"
TIMEOUT=3
TOSLEEP=0.1
radio = RFM69.RFM69(RF69_433MHZ, NODE, NET, True)
print "class initialized"

# Use the Broadcom SOC Pin numbers  
# Setup the Button Pin with Internal pullups enabled and PIN in reading mode.  
#GPIO.setmode(GPIO.BCM)  
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)  
GPIO.setup(ledpin, GPIO.OUT)

def Transmit(channel):
	print "Button pressed. Transmitting: " + msg
    	if radio.sendWithRetry(1, msg, 1, 5):
        	print "Ack recieved"

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

# Add Falling Edge Callback
GPIO.add_event_detect(pin, GPIO.FALLING, callback = Transmit, bouncetime = 5000) 

print "starting loop to wait"
sequence = 0
# Now wait!  
while 1:  
#    print "LED On"
    GPIO.output(ledpin,GPIO.HIGH)
    time.sleep(0.5)  
#    print "LED Off"
    GPIO.output(ledpin,GPIO.LOW)
    time.sleep(0.5)
#while True:
#
#   
#   sequence = sequence + 1
#
#   print "start recv..."
#   radio.receiveBegin()
#  timedOut=0
#   while not radio.receiveDone():
#       timedOut+=TOSLEEP
#       time.sleep(TOSLEEP)
#	if timedOut > TIMEOUT:
#            print "timed out waiting for recv"
#            break
#
#    print "end recv..."
#    print " *** %s from %s RSSI:%s" % ("".join([chr(letter) for letter in radio.DATA]), radio.SENDERID, radio.RSSI)
#
#    if radio.ACKRequested():
#        print "sending ack..."
#        radio.sendACK()
#    else:
#        print "ack not requested..."
#
#print "shutting down"
#radio.shutdown()
