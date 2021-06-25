from rpi_ws281x import *
import time
import multiprocessing

# LED strip configuration:
LED_COUNT = 48      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53 else 0


class LED:

    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.runInstance = multiprocessing.Process(target=self.startShow)
        self.runInstance.start()
        self.on = True

    def start(self):
        if self.runInstance.is_alive():
            self.runInstance.kill()
        self.runInstance = multiprocessing.Process(target=self.startShow)
        self.runInstance.start()
        self.on = True

    def startShow(self):
        while True:
            print('Color wipe animations.')
            self.colorWipe(Color(255, 0, 0), 20)  # Red wipe
            self.colorWipe(Color(0, 255, 0), 20)  # Blue wipe
            self.colorWipe(Color(0, 0, 255), 20)  # Green wipe
            print('Rainbow animations.')
            self.rainbow()
            self.rainbowCycle()

    def clearLedStrip(self):
        if self.runInstance.is_alive():
            self.runInstance.kill()
        self.colorWipe(Color(0, 0, 0), 10)
        self.on = False

    def getState(self) -> bool:
        return self.on

    def colorWipe(self, color, wait_ms=50):
        # Wipe color across display a pixel at a time.
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbow(self, wait_ms=20, iterations=1):
        # Draw rainbow that fades across all pixels at once.
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        # Draw rainbow that uniformly distributes itself across all pixels.
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(
                    i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def wheel(self, pos):
        # Generate rainbow colors across 0-255 positions.
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
