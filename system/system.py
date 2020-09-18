#!/usr/bin/env python
import pika
import threading
from time import sleep
from sensor import Sensor
import json


class Station:
    def __init__(self):
        self.interval = 30
        self.sensors = []
        self.machine_t = threading.Thread(target=self.reading_loop)
        self.machine_t.start()
        self.comm_t = threading.Thread(target=self.communicate)
        self.comm_t.start()

    def communicate(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpc_queue')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):
        request_type, data = (body.decode('ascii')).split('/')
        data = json.loads(data)
        sensor = Sensor(data['max'], data['min'], data['type'], data['id'])
        response = self.handle_request(request_type, sensor)
        print(response)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def handle_request(self, request_type, sensor):
        response = ''
        if request_type == 'PUT':
            sensor_ref = self.get_sensor(sensor)
            print(" Updating sensor" + str(sensor_ref.id))
            response = sensor_ref.write(sensor)
        elif request_type == 'POST':
            print(" Adding sensor" + str(sensor.id))
            self.sensors.append(sensor)
            response = sensor.active()
        elif request_type == 'DEL':
            response = True
        elif request_type == 'GET':
            sensor_ref = self.get_sensor(sensor)
            print(" Reading sensor" + str(sensor_ref.id))
            response = sensor_ref.read()
        return response

    def get_sensor(self, sensor):
        for s in self.sensors:
            if s.id == sensor.id:
                return s

    def notify(self, sensor_id, val):
        print("Notifying for sensor " + str(sensor_id) + " val " + str(val))

    def reading_loop(self):
        while True:
            for sensor in self.sensors:
                val = sensor.read()
                if val > sensor.max:
                    self.notify(sensor.id, val)
            sleep(self.interval)


if __name__ == '__main__':
    station = Station()
    station.comm_t.join()
    station.machine_t.join()