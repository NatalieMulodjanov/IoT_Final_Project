import RPi.GPIO as GPIO
import time

LEDPIN = 23

def setLED(option):
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LEDPIN,GPIO.OUT)
        if option == True:
            GPIO.output(LEDPIN,GPIO.HIGH)
            print("LED IS ON")
            time.sleep(2)
            GPIO.cleanup()
        else:
            GPIO.output(LEDPIN,GPIO.LOW)
            GPIO.cleanup()
    except:
            GPIO.output(LEDPIN,GPIO.LOW)
            GPIO.cleanup()