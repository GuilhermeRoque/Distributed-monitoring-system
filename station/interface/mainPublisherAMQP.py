#!/usr/bin/python3
import logging
import pika
from publisherAMQP import Publisher
from amqpConn import LOG_FORMAT
from flaskApp import db_conn

if __name__ == '__main__':
    db_conn.create_all()
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    credentials = pika.PlainCredentials('anderson.gm05', 'uL3tD8wV7lJ7nV2q')
    params = pika.ConnectionParameters(host='rabbitmq.sj.ifsc.edu.br', virtual_host='290pji06', credentials=credentials)
    publisher = Publisher(params)
    publisher.run()
