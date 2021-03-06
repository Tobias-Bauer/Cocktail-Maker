import RPi.GPIO as GPIO
import time
dict = {' 1': 'a', '2': 'b',  '4': 'c', '5': 'd', '5': 'e'}
print(('There are duplicates' if len(set(dict.values()))
       != len(dict.values()) else 'No duplicates'))

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)
# GPIO.output(4, GPIO.LOW)
# time.sleep(2)
# GPIO.cleanup()
