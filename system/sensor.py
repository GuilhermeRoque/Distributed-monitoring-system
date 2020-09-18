import threading
from ios import IOs


class Sensor:
    def __init__(self, max, min, type, id):
        self.io = IOs()
        self.max = max
        self.min = min
        self.type = type
        self.id = id
        self.mutex = threading.Lock()

    def active(self):
        return True

    def read(self):
        self.mutex.acquire(blocking=True)
        val = self.io.read()
        self.mutex.release()
        return val

    def write(self, data):
        self.mutex.acquire(blocking=True)
        val = self.io.write(data)
        self.mutex.release()
        return val