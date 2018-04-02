# -*- coding: utf-8 -*-
from model.crawl_fxssi import CrawlFxssi
from Controller import Controller
import json, re, requests, logging, datetime
from sqlalchemy import and_, or_, func

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/article.log',
                filemode='w')

class FxssiController(Controller):
    def __init__(self, topic="crawl_fxssi"):
        super(FxssiController, self).__init__(topic)

    def run(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))
            with self.session_scope(self.sess) as session:
                query = session.query(CrawlFxssi).filter(and_(
                    CrawlFxssi.created_at >= now
                )).delete()

                all_data = []
                for pair in data:
                    for broker in data[pair]:
                        fxssi = CrawlFxssi()
                        fxssi.broker = broker
                        fxssi.pair = pair
                        fxssi.val = data[pair][broker] if self.is_float(data[pair][broker]) else 50

                        all_data.append(fxssi)

                print all_data
                if all_data:
                    session.add_all(all_data)

    def is_float(self, num):
        try:
            float(num)
            return True
        except:
            return False
