#!/usr/bin/python3

import logging
import json
import threading
import pika
from amqpConn import AMQPConnection, LOGGER, LOG_FORMAT
from webApp import SensorDAO
from zmqRequest import ZMQRequest


class Publisher(AMQPConnection):
    EXCHANGE = 'logs'
    PUBLISH_INTERVAL = 1
    ROUTING_KEY = ''

    def __init__(self, broker):
        super().__init__(broker)
        self.interval = 30

    def start_publishing(self):
        LOGGER.info('Issuing consumer related RPC commands')
        self.schedule_next_message()

    def schedule_next_message(self):
        LOGGER.info('Scheduling next message for %0.1f seconds',
                    self.PUBLISH_INTERVAL)
        self._connection.ioloop.call_later(self.PUBLISH_INTERVAL,
                                           self.publish_message)

    def publish_message(self):

        if self._channel is None or not self._channel.is_open:
            return

        properties = pika.BasicProperties(
            app_id='example-publisher',
            content_type='application/json')

        self._channel.basic_publish(self.EXCHANGE, self.ROUTING_KEY,
                                    json.dumps(self.message, ensure_ascii=False),
                                    properties)

    def reading_loop(self):
        sensors = SensorDAO.query.all()
        LOGGER.info("Looping..")
        for sensor in sensors:
            sensor_json = sensor.to_json()
            LOGGER.info("Reading " + sensor_json['id'])
            request_json = {'cmd': 'GET'}
            request_json.update(sensor_json)
            response = ZMQRequest.talk_zmq(request_json)
            val = response
            LOGGER.info(response)
            if val[sensor.data_type] > sensor.max or val[sensor.data_type] < sensor.min:
                self.message = {'id': sensor.id, 'value': val}
                self.schedule_next_message()
        threading.Timer(self.interval, self.reading_loop).start()

    def start_working(self):
        threading.Timer(self.interval, self.reading_loop).start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    credentials = pika.PlainCredentials('anderson.gm05', 'uL3tD8wV7lJ7nV2q')
    params = pika.ConnectionParameters(host='rabbitmq.sj.ifsc.edu.br', virtual_host='290pji06', credentials=credentials)
    example = Publisher(params)
    example.run()
