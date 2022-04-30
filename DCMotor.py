import RPi.GPIO as GPIO
from time import sleep

enable = 4
pin1 = 27
pin2 = 22

def startMotor():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(enable, GPIO.OUT)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin1,1)
    GPIO.output(pin2,0)
    GPIO.output(enable,1)
    #sleep(1)
    #GPIO.output(enable,0)