import pika
import uuid
import json

class RpcClient(object):

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
    rpc = RpcClient()
    print('Adding sensor...')
    sensor = {"id": "sensor1", "max": 8, "min": 2, "type":"temp"}
    sensor_j = json.dumps(sensor)
    method = "POST"
    request = method+'/'+sensor_j
    response = rpc.call(request)
    print('Response: '+str(response))
    print('Reading sensor...')
    sensor_j = json.dumps(sensor)
    method = "GET"
    print('Response: '+str(response))

