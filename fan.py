from time import sleep
import RPi.GPIO as GPIO
def turnOnFan():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    enable=17
    pin1=26
    pin2=6                                                              

    GPIO.setup(enable, GPIO.OUT)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)

    GPIO.output(pin1, 1)
    GPIO.output(pin2, 0)
    pwm=GPIO.PWM(enable, 100)
    pwm.start(0)
    pwm.ChangeDutyCycle(50)
    GPIO.output(enable, 1)
    sleep(5)
    GPIO.output(enable, 0)
    GPIO.cleanup()