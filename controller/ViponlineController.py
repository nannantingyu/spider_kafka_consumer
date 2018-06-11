# -*- coding: utf-8 -*-
from model.crawl_vip_online import CrawlVipOnline
from Controller import Controller
import json, re, requests, logging, datetime, time
from sqlalchemy import and_, or_, func

class ViponlineController(Controller):
    def __init__(self, topic="crawl_vip_online"):
        super(ViponlineController, self).__init__(topic, 'vip_online')

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                all_data = []
                print data
                all_data.append(CrawlVipOnline(**data))

                if all_data:
                    with self.session_scope(self.sess) as session:
                        session.add_all(all_data)
            except:
                self.logger.error('Catch an exception.', exc_info=True)
                continue