#keypad tester

import RPi.GPIO as GPIO
import time

#from matrixKeypad_MCP230xx import keypad
from keypad_functions import keypad
#from time import sleep
 
# Initialize the keypad class
kp = keypad()
 
def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r 
 
print "Please enter a 4 digit code: "
 
# Getting digit 1, printing it, then sleep to allow the next digit press.
d1 = digit()
print d1
time.sleep(1)
 
d2 = digit()
print d2
time.sleep(1)
 
d3 = digit()
print d3
time.sleep(1)
 
d4 = digit()
print d4
 
# printing out the assembled 4 digit code.
print "You Entered %s%s%s%s "%(d1,d2,d3,d4) 
