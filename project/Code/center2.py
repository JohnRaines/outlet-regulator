#**************************************************
#This file contains the main method and calls the
#other files
#
#Author: John Raines
#Date: 29 - 12 - 16 (dd mm yy)
#
#change log: added monitor status checking and
#extra courtesy messages when you put in a code
#**************************************************

#imports
import time
import web_scrape
import lcd_functions
import RPi.GPIO as GPIO
import signal
from keypad_functions import keypad

#init keypad and strngs
kp = keypad()   #keypad object
message = ""    #holds the "next job" message on the top line
pintext = ""    #holds the "enter pin: xxxxx" message on the bottom line
code = ""       #holds the code that was input
packet = ""     #the input code and the machine code  that are sent to the site
sixflag = False #used to check if 6 digits have been entered
machine = ""    #holds the machine code character


#redundant pin assignments
LCD_RS = 14
LCD_E  = 15
LCD_D4 = 18
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25

#non redundant pin assignments
MONITOR = 22

def main():
    global message,pintext
    
    print "working"
    pin_setup()
    lcd_functions.lcd_init()
    getmachine()
    
    next_job = web_scrape.get_site()
    marquee = next_job
    message = "Next Job: " + next_job[:6]
    pintext = "EnterPin: "
    lcd_update(message,pintext)
    
    while True:
        #check if the next job has updated
        if next_job != web_scrape.get_site():
            next_job = web_scrape.get_site()
            marquee = next_job

        #print message and scroll the marquee    
        message = "Next Job: " + marquee[:6]
        lcd_update(message, pintext)
        #marquee = marquee[1:] + marquee[0]
        delay()
        if sixflag == True:
            fling()
        message = "Next Job: " + marquee[7:]
        lcd_update(message,pintext)
        delay()
        if sixflag == True:
            fling()

def pin_setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(MONITOR, GPIO.OUT)# relay control pin

def lcd_update(top, bottom):
    lcd_functions.lcd_string(top, 0X80)
    lcd_functions.lcd_string(bottom, 0xC0)

#delays updates so you can read the screen and reads from the keypad
def delay():
    global message,pintext,code,sixflag

    #nested for loop delay cycle
    for i in range(10):
        for j in range(1000):
            #reset the key to null, then fetch a value for key
                    key_get()
                    if sixflag == True:
                        return
                    

        j+=1
    i+=1

#for getting the key and handling clearing
def key_get():
    global pintext, sixflag, code
    
    key = None
    key = kp.getKey()
    if key != None:
       # #is the clear key, so check if that was the one pressed
       if key != "#":
           pintext += str(key)
           code += str(key)
           lcd_update(message,pintext)
           time.sleep(.3)
           if len(code) == 6:
               sixflag = True
       else:
           pintext = "EnterPin: "
           code = ""
           lcd_update(message,pintext)
           time.sleep(.3)
    
#relays the code input to the server
def fling():
    global code,sixflag,machine,message,pintext
    sixflag = False #clear the flag
    confirm = 0     #clear the confirm choice variable
    lcd_update("Is " + code + " right?", "*= yes #= no")
    print machine + code #print the code to the command line for debug purposes
    #get keypress
    while confirm != 1:
        press = kp.getKey()
        if press == "#" or press == "*":
            confirm = 1
    #interpret key pressed
    if press == "#":
        code = ""
        pintext = "EnterPin: "
    else:
        code = ""   #clear code after entering
        pintext= "EnterPin: "
        lcd_update("Processing...", "Please Wait")  #stall for time
        time.sleep(3)
        monitor_check() #check if the mointor is on
        #remind people to sign out when done
        lcd_update("Please sign out", "when done")
        time.sleep(3)
        
        

def getmachine():
    #a txt with a single character is used to differentiate the machines
    #this pulls the character from the text file on the sd card
    #the character is prepended to whatever code is entered on the pad
    global machine
    file = open("machine.txt", 'r')
    machine = str(file.read(1))

def monitor_check():
    #monitor on or off is determined by a 1 or 0 on the site
    monitor = web_scrape.get_status()
    if monitor == "1":
        print "monitor is on"
        GPIO.output(MONITOR, GPIO.HIGH)
    else:
        print "monitor is off"
        GPIO.output(MONITOR, GPIO.LOW)

main()
