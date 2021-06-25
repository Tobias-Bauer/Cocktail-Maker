# e.g.: mix(ingredients, ml)

import RPi.GPIO as GPIO
import time
import json
pumps = json.load(open("pumps.json"))


class Pumps:

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        for pump in pumps:
            GPIO.setup(pump["gpio"], GPIO.OUT, initial=GPIO.HIGH)

    def toggle(self, pumpNum):
        gpio = 0
        for pump in pumps:
            if pump['num'] == pumpNum:
                gpio = pump['gpio']
        if GPIO.input(gpio):
            GPIO.output(gpio, GPIO.LOW)
        else:
            GPIO.output(gpio, GPIO.HIGH)

    def clean(self):
        GPIO.cleanup()


l = Pumps()
l.toggle(4)
time.sleep(10)
l.toggle(4)

# model 1: 1s ≈ 5,4ml
