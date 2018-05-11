# -*- coding: utf-8 -*-
from model.crawl_cftc import CrawlCftc
from kafka import KafkaConsumer
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

class NiuyanController(Controller):
    def __init__(self, topic="niuyan_hangqing"):
        super(NiuyanController, self).__init__(topic, 'niuyan_hangqing')

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))
            print data