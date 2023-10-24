import time
import RPi.GPIO as GPIO

## Inputs / Outputs
PIN_REL_1 = 22
PIN_REL_2 = 23
PIN_REL_3 = 24
PIN_REL_4 = 25
PIN_RAIN = 27

## GPIO definitionen
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_REL_1,GPIO.OUT)
GPIO.output(PIN_REL_1,GPIO.LOW)
GPIO.setup(PIN_REL_2,GPIO.OUT)
GPIO.output(PIN_REL_2,GPIO.LOW)
GPIO.setup(PIN_REL_3,GPIO.OUT)
GPIO.output(PIN_REL_3,GPIO.LOW)
GPIO.setup(PIN_REL_4,GPIO.OUT)
GPIO.output(PIN_REL_4,GPIO.LOW)
GPIO.setup(PIN_RAIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)

class Shuttercontrol():
    def shutterSouthIn(self):
        GPIO.output(PIN_REL_1,GPIO.HIGH)
        time.sleep(.6)
        GPIO.output(PIN_REL_1,GPIO.LOW)
        print("shutterSouthIn")
    def shutterSouthOut(self):
        GPIO.output(PIN_REL_2,GPIO.HIGH)
        time.sleep(.6)
        GPIO.output(PIN_REL_2,GPIO.LOW)
        print("shutterSouthOut")
    def shutterWestUp(self):
        GPIO.output(PIN_REL_3,GPIO.HIGH)
        time.sleep(.4)
        GPIO.output(PIN_REL_3,GPIO.LOW)
        print("shutterWestUp")
    def shutterWestDown(self):
        GPIO.output(PIN_REL_4,GPIO.HIGH)
        time.sleep(.4)
        GPIO.output(PIN_REL_4,GPIO.LOW)
        print("shutterWestDown")
    def isItRaining(self):
        if GPIO.input(PIN_RAIN)==1:
            print("It isn't raining!")
            return False
        if GPIO.input(PIN_RAIN)==0:
            print("It is raining!")
            return True
        return True
