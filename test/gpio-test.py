#!/usr/bin/env python3          
                                
import signal                   
import sys
import time
import RPi.GPIO as GPIO


SH_H_UP = 22
SH_H_DN = 23
SH_V_UP = 24
SH_V_DN = 25

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SH_H_UP, GPIO.OUT)   
    GPIO.setup(SH_H_DN, GPIO.OUT)   
    GPIO.setup(SH_V_UP, GPIO.OUT)   
    GPIO.setup(SH_V_DN, GPIO.OUT)   
    time.sleep(1)
    GPIO.output(SH_H_UP, GPIO.HIGH) 
    time.sleep(1)
    GPIO.output(SH_H_UP, GPIO.LOW)
    time.sleep(1)
    GPIO.output(SH_H_DN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(SH_H_DN, GPIO.LOW)
    time.sleep(1)
    GPIO.output(SH_V_UP, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(SH_V_UP, GPIO.LOW)
    time.sleep(1)
    GPIO.output(SH_V_DN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(SH_V_DN, GPIO.LOW)

exit(0)
