#!/usr/bin/python3
import pika


class AMQPListen:
    def __init__(self):
        credentials = pika.PlainCredentials('anderson.gm05', 'uL3tD8wV7lJ7nV2q')
        self.broadcast_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq.sj.ifsc.edu.br', virtual_host='290pji06', credentials=credentials))
        self.broadcast_channel = self.broadcast_connection.channel()
        self.broadcast_channel.exchange_declare(exchange='logs', exchange_type='fanout')
        result = self.broadcast_channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.broadcast_channel.queue_bind(exchange='logs', queue=queue_name)
        self.broadcast_channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)

    def callback(self, ch, method, props, body):
        print("Received Notification: " + body.decode("ascii"))

    def run(self):
        try:
            self.broadcast_channel.start_consuming()
        except:
            pass


if __name__ == '__main__':
    user = AMQPListen()
    user.run()
