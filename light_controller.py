import RPi.GPIO as GPIO


class Lights:

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)

    def lightToGPIO(self, lightNum):
        if(lightNum < 7 and lightNum > 0):
            lightConf = [4, 6, 23, 24, 25, 12]
            return lightConf[lightNum-1]

    def toggle(self, lightNum):
        if GPIO.input(self.lightToGPIO(lightNum)):
            GPIO.output(self.lightToGPIO(lightNum), GPIO.LOW)
        else:
            GPIO.output(self.lightToGPIO(lightNum), GPIO.HIGH)

    def clean(self):
        GPIO.cleanup()
