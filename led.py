import RPi.GPIO as GPIO
import time

LEDPIN = 17

def setLED(option):
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LEDPIN,GPIO.OUT)
        if option == True:
            GPIO.output(LEDPIN,GPIO.HIGH)
        else:
            GPIO.output(LEDPIN,GPIO.LOW)
    except:
            GPIO.output(LEDPIN,GPIO.LOW)