import pika


class User:
    def __init__(self):
        self.broadcast_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
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
    user = User()
    user.run()
