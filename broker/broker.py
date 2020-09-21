import pika
import uuid
import json
import threading
from random import randint
from time import sleep


class Broker:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.rpc_t = threading.Thread(target=self.rpc_loop)

    def run(self):
        self.rpc_t.start()
        self.rpc_t.join()

    def rpc_loop(self):
        print('Adding sensor...')
        sensor = {"id": "sensor1", "max": 6, "min": 3, "type": "temp"}
        sensor_j = json.dumps(sensor)
        request = "POST" + '/' + sensor_j
        response = self.call(request)
        print('Response: ' + str(response))

        while True:
            sleep(randint(1, 10))
            print('Request reading sensor...')
            sensor_j = json.dumps(sensor)
            request = "GET" + '/' + sensor_j
            response = self.call(request)
            print('Response: ' + str(response))

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode('ascii')

    def call(self, data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(data))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


if __name__ == '__main__':
    broker = Broker()
    broker.run()
