import time
import RPi.GPIO as GPIO

## Inputs / Outputs
PIN_REL_1 = 22
PIN_REL_2 = 23
PIN_REL_3 = 24
PIN_REL_4 = 25
PIN_WIND = 19
PIN_RAIN = 20
PIN_SUNNY = 21

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

GPIO.setup(PIN_WIND,GPIO.OUT)
GPIO.output(PIN_WIND,GPIO.LOW)
GPIO.setup(PIN_RAIN,GPIO.OUT)
GPIO.output(PIN_RAIN,GPIO.LOW)
GPIO.setup(PIN_SUNNY,GPIO.OUT)
GPIO.output(PIN_SUNNY,GPIO.LOW)

#GPIO.setup(PIN_WIND,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(PIN_RAIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(PIN_SUNNY,GPIO.IN,pull_up_down=GPIO.PUD_UP)

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
    def isItWindy(self):
        if GPIO.input(PIN_WIND)==1:
            print("It isn't windy!")
            return False
        if GPIO.input(PIN_WIND)==0:
            print("It is windy!")
            return True
        return True
    def isItSunny(self):
        if GPIO.input(PIN_SUNNY)==1:
            print("It isn't sunny!")
            return False
        if GPIO.input(PIN_SUNNY)==0:
            print("It is sunny!")
            return True
        return False
