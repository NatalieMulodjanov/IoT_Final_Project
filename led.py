import RPi.GPIO as GPIO
import time

def setLED(option):
    try:        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17,GPIO.OUT)
        if option == True:
            GPIO.output(17,GPIO.HIGH)
        else:
            GPIO.output(17,GPIO.LOW)
    except:        
        GPIO.cleanup()
        setLED(option)
