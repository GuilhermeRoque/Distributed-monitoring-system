import Adafruit_DHT
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
from sensor import Sensor
from random import randint


class DHT11(Sensor):

    def __init__(self, sensor_dict, **kwargs):
        super().__init__(sensor_dict, **kwargs)
        self.pin = kwargs.pop('pin')

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self.pin)
        values = {'humidity': humidity, 'temperature': temperature}
        # values = {'humidity': randint(1, 10), 'temperature': randint(1, 10)}
        return values

    def activate(self):
        return 1
