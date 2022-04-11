#!/usr/bin/env python3
#############################################################################
# Filename    : DHT11.py
# Description :	read the temperature and humidity data of DHT11
# Author      : freenove
# modification: 2020/10/16
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

DHTPin = 11      #define the pin of DHT11


def loop():
    try:
        dht = DHT.DHT(DHTPin)
        chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        if (chk is not dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            return 0,0
        return dht.humidity,dht.temperature
    except:
        GPIO.cleanup()
        loop()