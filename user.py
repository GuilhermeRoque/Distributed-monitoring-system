import pika

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='q1')
    channel.basic_publish(exchange='',
                          routing_key='q1',
                          body='Hello World3!')
    print(" [x] Sent 'Hello World!'")
    connection.close()