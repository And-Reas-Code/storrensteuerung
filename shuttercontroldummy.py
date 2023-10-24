import time

class Shuttercontrol():
    def shutterSouthIn(self):
        time.sleep(.2)
        print("shutterSouthIn")
    def shutterSouthOut(self):
        time.sleep(.2)
        print("shutterSouthOut")
    def shutterWestUp(self):
        time.sleep(.2)
        print("shutterWestUp")
    def shutterWestDown(self):
        time.sleep(.2)
        print("shutterWestDown")
    def isItRaining(self):
        print("It is raining!")
        return True
   