from sensor import Sensor
from random import randint


class BMP280(Sensor):

    def __init__(self, sensor_dict, **kwargs):
        super().__init__(sensor_dict, **kwargs)

    def read(self):
        values = {'pressure': randint(1, 10), 'temperature': randint(1, 10), 'altitude': randint(1, 10)}
        return values

    def activate(self):
        return 1
