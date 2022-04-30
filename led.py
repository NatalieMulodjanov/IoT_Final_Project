import RPi.GPIO as GPIO
import time

LEDPIN = 23

def setLED():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDPIN,GPIO.OUT)
    GPIO.output(LEDPIN,GPIO.HIGH)
    print("LED IS ON")