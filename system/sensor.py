import threading
from sensorIO import SensorIO


class Sensor(SensorIO):
    def __init__(self, sensor_dict, **kwargs):
        self.max = sensor_dict['max']
        self.min = sensor_dict['min']
        self.type = sensor_dict['type']
        self.id = sensor_dict['id']
        self.mutex = threading.Lock()

    def __repr__(self):
        return '<Sensor {}>'.format(self.id)
