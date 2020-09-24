#! /home/guilherme/PycharmProjects/broker/venv/bin/python
import pika
import sys, getopt

class AMQPListen:
    def __init__(self, IP):
        self.broadcast_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=IP))
        self.broadcast_channel = self.broadcast_connection.channel()
        self.broadcast_channel.exchange_declare(exchange='logs', exchange_type='fanout')
        result = self.broadcast_channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.broadcast_channel.queue_bind(exchange='logs', queue=queue_name)
        self.broadcast_channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)

    def callback(self, ch, method, props, body):
        print("Received Notification: " + body.decode("ascii"))

    def run(self):
        self.broadcast_channel.start_consuming()

    def __del__(self):
        self.broadcast_connection.close()


if __name__ == '__main__':
    IP = ''
    usage_message = """
Usage:
amqp-listen.py -i <IP>
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:", ["IP ="])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)
    if not len(opts):
        print(usage_message)
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-h':
            print(usage_message)
            sys.exit()
        elif opt in ("-i", "--IP"):
            IP = arg

    user = AMQPListen(IP)
    user.run()

