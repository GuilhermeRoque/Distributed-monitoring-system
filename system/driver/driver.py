#!/usr/bin/python3
import zmq
from dht11 import DHT11

context = zmq.Context()
HOST = "*"
PORT = "50007"
p = "tcp://" + HOST + ":" + PORT
socket = context.socket(zmq.REP)
socket.bind(p)


class SensorDriver:

    @staticmethod
    def loop4ever():
        while True:
            json_msg = socket.recv_json()
            cmd = json_msg.pop('cmd')
            model = json_msg['model']
            sensor = None
            if model == 'DHT11':
                sensor = DHT11(json_msg, pin=json_msg['type_specific']['pin'])
            if cmd == 'GET':
                response = sensor.read()
                socket.send_json(response)
            elif cmd == 'POST':
                response = sensor.activate()
                socket.send_json({"ack": response})


if __name__ == '__main__':
    SensorDriver.loop4ever()
