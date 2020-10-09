#!/usr/bin/python3

import functools
import json
import logging
import pika
from amqpConn import AMQPConnection, LOGGER, LOG_FORMAT
from webApp import SensorDAO, db_conn
from zmqRequest import ZMQRequest


class Consumer(AMQPConnection):
    def __init__(self, broker):
        super().__init__(broker)
        self._prefetch_count = 1
        self.QUEUE = 'rpc_queue'

    def after_channel_opened(self):
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        LOGGER.info('Declaring queue %s', queue_name)
        cb = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(queue=queue_name, callback=cb)

    def on_queue_declareok(self, _unused_frame, userdata):
        self.set_qos()

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        LOGGER.info('QOS set to: %d', self._prefetch_count)
        self._channel.basic_consume(self.QUEUE, on_message_callback=self.on_request)

    def on_request(self, ch, method, props, body):
        body_str = body.decode('ascii')
        logging.info("Received request: " + body_str)
        request_type, data = body_str.split('/')
        data = json.loads(data)
        response = self.handle_request(request_type, data)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def handle_request(self, request_type, data):
        response = 'Error'
        try:
            if request_type == 'PUT':
                SensorDAO.query.filter_by(id=data['id']).update({'max': data['max'],
                                                                 'min': data['min'],
                                                                 'data_type': data['data_type']})
                db_conn.session.commit()
                response = {'ack': 1}
            elif request_type == 'GET':
                sensorD = SensorDAO.query.filter_by(id=data['id']).first()
                request_json = sensorD.to_json()
                request_json['cmd'] = request_type
                response = ZMQRequest.talk_zmq(request_json)
        except Exception as e:
            print(e)
        return response


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    credentials = pika.PlainCredentials('anderson.gm05', 'uL3tD8wV7lJ7nV2q')
    params = pika.ConnectionParameters(host='rabbitmq.sj.ifsc.edu.br', virtual_host='290pji06', credentials=credentials)
    example = Consumer(params)
    example.run()
