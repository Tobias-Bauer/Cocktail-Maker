import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.output(4, GPIO.LOW)
time.sleep(2)
GPIO.cleanup()
