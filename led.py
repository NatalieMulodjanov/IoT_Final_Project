import RPi.GPIO as GPIO
import time

def setLED(option):
    LEDPIN = 21
    try:        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LEDPIN,GPIO.OUT)
        if option == True:
            GPIO.output(LEDPIN,GPIO.HIGH)
        else:
            GPIO.output(LEDPIN,GPIO.LOW)
    except:        
        GPIO.cleanup()
        setLED(option)
