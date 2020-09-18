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

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = self.connection.channel()
        channel.queue_declare(queue='rpc_queue')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)

        self.broadcast_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.broadcast_channel = self.broadcast_connection.channel()

        self.machine_t = threading.Thread(target=self.reading_loop)
        self.comm_t = threading.Thread(target=channel.start_consuming)

    def __del__(self):
        self.connection.close()

    def run(self):
        self.machine_t.start()
        self.comm_t.start()
        self.comm_t.join()
        self.machine_t.join()

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
            print(" Updating sensor: " + str(sensor_ref.id))
            response = sensor_ref.write(sensor)
        elif request_type == 'POST':
            print(" Adding sensor: " + str(sensor.id))
            self.sensors.append(sensor)
            response = sensor.active()
        elif request_type == 'DEL':
            response = True
        elif request_type == 'GET':
            sensor_ref = self.get_sensor(sensor)
            print("Reading sensor: " + str(sensor_ref.id))
            response = sensor_ref.read()
        return response

    def get_sensor(self, sensor):
        for s in self.sensors:
            if s.id == sensor.id:
                return s

    def notify(self, sensor_id, val):
        print("Notifying for sensor: " + str(sensor_id) + " val " + str(val))
        message = str(sensor_id) + ":" + str(val)
        self.broadcast_channel.basic_publish(exchange='logs', routing_key='', body=message)

    def reading_loop(self):
        while True:
            for sensor in self.sensors:
                print("Looping reading sensor: ")
                val = sensor.read()
                print(val)
                if val > sensor.max or val < sensor.min:
                    self.notify(sensor.id, val)
            sleep(self.interval)


if __name__ == '__main__':
    station = Station()
    station.run()
