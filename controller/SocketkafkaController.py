# -*- coding: utf-8 -*-
from Controller import Controller
import json, re, requests, logging
from socketIO_client import SocketIO, LoggingNamespace
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/socketkafka.log',
                filemode='w')

class SocketkafkaController(Controller):
    def __init__(self, topic=""):
        super(SocketkafkaController, self).__init__(topic)

    def on_connect(self):
        print('connect')

    def on_disconnect(self):
        print('disconnect')

    def on_reconnect(self):
        print('reconnect')

    def on_aaa_response(self, *args):
        print('on_aaa_response', args)

    def run(self):
        socketIO = SocketIO('127.0.0.1', 8002, LoggingNamespace)
        socketIO.on('connect', self.on_connect)
        socketIO.on('disconnect', self.on_disconnect)
        socketIO.on('reconnect', self.on_reconnect)

        server = {
            'host': '192.168.100.131:9092,192.168.100.132:9092,192.168.100.133:9092',
        }

        consumer = KafkaConsumer('crawl_jin10_kuaixun',
                                 bootstrap_servers=server['host'],
                                 group_id='spider',
                                 auto_offset_reset="earliest")

        for msg in consumer:
            data = json.loads(msg.value.decode('utf-8'))
            print data
            socketIO.emit('kuaixun', msg.value.decode('utf-8'))