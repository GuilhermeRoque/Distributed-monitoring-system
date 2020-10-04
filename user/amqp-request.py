#! /home/guilherme/PycharmProjects/PJ2/venv/bin/python
import getopt
import json
import sys
import uuid
import pika

class AMQPRequest:
    def __init__(self, IP, method, id, max=None, min=None, type=None):

        credentials = pika.PlainCredentials('anderson.gm05', 'uL3tD8wV7lJ7nV2q')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=IP, virtual_host='290pji06', credentials=credentials))

        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        if method == 'GET':
            self.request = {"id": id}
        else:
            self.request = {"id": id, "max": int(max), "min": int(min), "type": type}
        self.request = method + '/' + json.dumps(self.request)
        print(self.request)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode('ascii')

    def send(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=self.request.encode('utf-8'))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


if __name__ == '__main__':
    IP = None
    id = None
    min = None
    max = None
    type = None
    method = None
    usage_message = """
Usage:
amqp-request.py -i <IP> -r <sensorID>
amqp-request.py -i <IP> -c <sensorID> -M <max> -m <min> -d <datatype> 
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:c:M:m:i:d:",
                                   ["read =", "configure =", "max =", "min =", "IP =", "datatype ="])
    except getopt.GetoptError as error:
        print(error)
        print(usage_message)
        sys.exit(2)
    if ('-r' in sys.argv[1:] or '--read' in sys.argv[1:]):
        for opt, arg in opts:
            if opt in ('-r', '--read'):
                id = arg
            elif opt in ("-i", "--IP"):
                IP = arg
        method = "GET"
    elif ('-c' in sys.argv[1:] or '--configure' in sys.argv[1:]) and \
            (('-M' in sys.argv[1:] or '--max' in sys.argv[1:]) and
             ('-m' in sys.argv[1:] or '--min' in sys.argv[1:]) and
             ('-d' in sys.argv[1:] or '--datatype' in sys.argv[1:])):
        for opt, arg in opts:
            if opt in ('-c', '--configure'):
                id = arg
            elif opt in ('-m', '--min'):
                min = arg
            elif opt in ('-M', '--max'):
                max = arg
            elif opt in ('-d', '--datatype'):
                type = arg
            elif opt in ("-i", "--IP"):
                IP = arg
        method = "PUT"
    else:
        print(usage_message)
        sys.exit(0)
    request = AMQPRequest(IP, method, id, max, min, type)
    resp = request.send()
    print(resp)
