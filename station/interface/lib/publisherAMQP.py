import json
import pika
from amqpConn import AMQPConnection, LOGGER
from flaskApp import SensorDAO
from zmqRequest import ZMQRequest


class Publisher(AMQPConnection):
    EXCHANGE = 'logs'
    PUBLISH_INTERVAL = 1
    ROUTING_KEY = ''
    READING_INTERVAL = 30

    def __init__(self, broker):
        super().__init__(broker)

    def start_publishing(self):
        LOGGER.info('Issuing consumer related RPC bin')
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
        self._connection.ioloop.call_later(self.READING_INTERVAL, self.reading_loop)

    def start_working(self):
        self._connection.ioloop.call_later(self.READING_INTERVAL, self.reading_loop)