#!/usr/bin/env python
import pika
import threading
from app import SensorDAO, sensors_list, db_conn
import json


class Station:
    def __init__(self):
        self.sensors = sensors_list
        self.interval = 30
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = self.connection.channel()
        channel.queue_declare(queue='rpc_queue')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)

        self.broadcast_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.broadcast_channel = self.broadcast_connection.channel()

        self.comm_t = threading.Thread(target=channel.start_consuming)

    def __del__(self):
        self.connection.close()

    def run(self):
        threading.Timer(self.interval, self.reading_loop).start()
        self.comm_t.start()

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
                sensor = self.get_sensor(data['id'])
                print(" Updating sensor: " + str(sensor.id))
                sensor.max = data['max']
                sensor.min = data['min']

                SensorDAO.query.filter_by(id=data['id']).update({'max': data['max'], 'min': data['min']})
                db_conn.session.commit()
                response = 'Success'
            elif request_type == 'GET':
                sensor_ref = self.get_sensor(data['id'])
                print("Reading sensor: " + str(sensor_ref.id))
                response = 'Value read from ' + data['id'] + ': ' + str(sensor_ref.read())

        except:
            pass
        return response

    def get_sensor(self, id):
        for s in self.sensors:
            if s.id == id:
                return s

    def notify(self, sensor_id, val):
        print("Notifying for sensor: " + str(sensor_id) + " val " + str(val))
        message = str(sensor_id) + ":" + str(val)
        self.broadcast_channel.basic_publish(exchange='logs', routing_key='', body=message)

    def reading_loop(self):
        for sensor in self.sensors:
            print("Looping reading sensor: ")
            val = sensor.read()
            if val['temperature'] > sensor.max or val['temperature'] < sensor.min:
                self.notify(sensor.id, val)
        threading.Timer(self.interval, self.reading_loop).start()


if __name__ == '__main__':
    station = Station()
    station.run()
    station.comm_t.join()
