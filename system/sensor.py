import threading
#from ios import IOs
from ios_dht11 import IOs_dht11

class Sensor:
    def __init__(self, sensor_dict):
        self.io = IOs_dht11()
        self.max = sensor_dict['max']
        self.min = sensor_dict['min']
        self.type = sensor_dict['type']
        self.id = sensor_dict['id']
        self.mutex = threading.Lock()

    def active(self):
        return True

    def read(self):
        self.mutex.acquire(blocking=True)
        #val = self.io.read()
        val = self.io.read_temperatura()
        self.mutex.release()
        return val

    def write(self, data):
        self.mutex.acquire(blocking=True)
        val = self.io.write(data)
        self.mutex.release()
        return val

    def __repr__(self):
        return '<Sensor {}>'.format(self.id)
