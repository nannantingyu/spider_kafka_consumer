# -*- coding: utf-8 -*-
from Controller import Controller
import json, re, requests, logging
from socketIO_client import SocketIO, LoggingNamespace
import redis


logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/socketredis.log',
                filemode='w')

class SocketredisController(Controller):
    def __init__(self, topic=""):
        super(SocketredisController, self).__init__(topic)

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

        r = redis.Redis(host="127.0.0.1", port=6379)
        p = r.pubsub()
        p.subscribe("crawl_jin10_kuaixun")
        for item in p.listen():
            print item
            try:
                data = json.loads(item['data'])
                print data
                socketIO.emit('crawl_jin10_kuaixun', data[0]['messages'])
            except Exception, e:
                print e