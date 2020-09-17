from system.system import IO
import threading


class Sensor:
    def __init__(self, max, min, type, id, io):
        self.io = IO()
        self.max = max
        self.min = min
        self.type = type
        self.mutex = threading.Lock()

    def read(self):
        self.mutex.acquire(blocking=True)
        val = self.io.read()
        self.mutex.release()
        return val

    def write(self):
        self.mutex.acquire(blocking=True)
        val = self.io.write()
        self.mutex.release()
        return val
