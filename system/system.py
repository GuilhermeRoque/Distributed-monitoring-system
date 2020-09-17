#!/usr/bin/env python
import pika
import threading
from time import sleep


class Station:
    def __init__(self):
        self.interval = 30
        self.machine_t = threading.Thread(target=self.reading_loop)
        self.machine_t.start()
        self.sensors = []

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rpc_queue')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)

    def on_request(self, ch, method, props, body):
        sensor_id = int(body)
        print(" Reading sensor" + str(sensor_id))

        val = self.sensors[sensor_id].sensor.read()
        response = val

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def notify(self, sensor_id, val):
        pass

    def register(self):
        pass

    def reading_loop(self):
        while True:
            for sensor in self.sensors:
                val = sensor.read()
                if val > sensor.max:
                    self.notify(sensor.id, val)


if __name__ == '__main__':
    pass
