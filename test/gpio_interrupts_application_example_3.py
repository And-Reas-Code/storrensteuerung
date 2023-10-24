#!/usr/bin/env python3          
                                
import signal                   
import sys
import time
import RPi.GPIO as GPIO

BUTTON_GPIO = 27
REL_1_GPIO = 22
REL_2_GPIO = 23
REL_3_GPIO = 24
REL_4_GPIO = 25

should_blink = False

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_released_callback(channel):
    global should_blink
    should_blink = not should_blink  
    print("BUTTON-RELEASED")

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(REL_1_GPIO, GPIO.OUT)   
    GPIO.setup(REL_2_GPIO, GPIO.OUT)   
    GPIO.setup(REL_3_GPIO, GPIO.OUT)   
    GPIO.setup(REL_4_GPIO, GPIO.OUT)   

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING,callback=button_released_callback, bouncetime=200)

    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        if should_blink:
            GPIO.output(REL_1_GPIO, GPIO.HIGH) 
            GPIO.output(REL_2_GPIO, GPIO.HIGH) 
            GPIO.output(REL_3_GPIO, GPIO.HIGH) 
            GPIO.output(REL_4_GPIO, GPIO.HIGH) 
        time.sleep(0.5)
        if not should_blink:
            GPIO.output(REL_1_GPIO, GPIO.LOW)  
            GPIO.output(REL_2_GPIO, GPIO.LOW)  
            GPIO.output(REL_3_GPIO, GPIO.LOW)  
            GPIO.output(REL_4_GPIO, GPIO.LOW)  
        time.sleep(0.5)

