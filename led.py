import RPi.GPIO as GPIO
import time

LEDPIN = 12

def setLED(option):
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LEDPIN,GPIO.OUT)
        if option == True:
            GPIO.output(LEDPIN,GPIO.HIGH)
            print("LED IS ON")
            GPIO.cleanup()
        else:
            GPIO.output(LEDPIN,GPIO.LOW)
            GPIO.cleanup()
    except:
            GPIO.output(LEDPIN,GPIO.LOW)
            GPIO.cleanup()