#!/usr/bin/env python
import pika
import threading
from webApp import SensorDAO, db_conn
import json
from zmqRequest import ZMQRequest


class Station:
    def __init__(self):
        self.interval = 30
        credentials = pika.PlainCredentials('anderson.gm05', 'uL3tD8wV7lJ7nV2q')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq.sj.ifsc.edu.br', virtual_host='290pji06', credentials=credentials))

        channel = self.connection.channel()
        channel.queue_declare(queue='rpc_queue')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)

        self.broadcast_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq.sj.ifsc.edu.br', virtual_host='290pji06', credentials=credentials))
        self.broadcast_channel = self.broadcast_connection.channel()

        self.comm_t = threading.Thread(target=channel.start_consuming)

    def __del__(self):
        self.connection.close()

    def run(self):
        threading.Timer(self.interval, self.reading_loop).start()
        self.comm_t.start()
        self.comm_t.join()

    def on_request(self, ch, method, props, body):
        request_type, data = (body.decode('ascii')).split('/')
        data = json.loads(data)
        print(data)
        print(request_type)
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
        except:
            pass
        return response

    def notify(self, sensor_id, val):
        print("Notifying for sensor: " + str(sensor_id) + " val " + str(val))
        message = str(sensor_id) + ":" + str(val)
        self.broadcast_channel.basic_publish(exchange='logs', routing_key='', body=message)

    def reading_loop(self):
        sensors = SensorDAO.query.all()
        print("Looping..")
        for sensor in sensors:
            sensor_json = sensor.to_json()
            print("Reading " + sensor_json['id'])
            request_json = {'cmd': 'GET'}
            request_json.update(sensor_json)
            response = ZMQRequest.talk_zmq(request_json)
            val = response
            print(response)
            if val[sensor.data_type] > sensor.max or val[sensor.data_type] < sensor.min:
                self.notify(sensor.id, val)
        threading.Timer(self.interval, self.reading_loop).start()


if __name__ == '__main__':
    station = Station()
    station.run()
