#**************************************************
#This file contains the main method and calls the
#other files
#
#Author: John Raines
#Date: 14 - 12 - 16 (dd mm yy)
#**************************************************

#imports
import time
import web_scrape
import lcd_functions
import RPi.GPIO as GPIO

#redundant pin assignments
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

def main():
    print "working"
    pin_setup()
    lcd_functions.lcd_init()
    next_job = web_scrape.get_site()
    #marquee = next_job + " "
    marquee = next_job
    message = "Next Job: " + next_job[:6]
    lcd_functions.lcd_string(message,0x80)
    lcd_functions.lcd_string("EnterPin: ",0xC0)
    while True:
        #check if the next job has updated
        if next_job != web_scrape.get_site():
            next_job = web_scrape.get_site()
            #marquee = next_job + " "
            marquee = next_job

        #print message and scroll the marquee    
        message = "Next Job: " + marquee[:6]
        lcd_functions.lcd_string(message,0x80)
        #marquee = marquee[1:] + marquee[0]
        time.sleep(1.3)
        message = "Next Job: " + marquee[7:]
        lcd_functions.lcd_string(message,0x80)
        time.sleep(1.3)

def pin_setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7

main()
