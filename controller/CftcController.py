# -*- coding: utf-8 -*-
from model.crawl_cftc import CrawlCftc
from kafka import KafkaConsumer
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/article.log',
                filemode='w')

class CftcController(Controller):
    def __init__(self, topic="crawl_cftc"):
        super(CftcController, self).__init__(topic)

    def run(self):
        for msg in self.consumer:
	    print msg
            data = json.loads(msg.value.decode('utf-8'))
            cftc = CrawlCftc(**data)
            with self.session_scope(self.sess) as session:
                query = session.query(CrawlCftc.id).filter(
                    and_(
                        CrawlCftc.cftc_name == cftc.cftc_name, CrawlCftc.publish_time == cftc.publish_time
                    )
                ).one_or_none()

                if query is None:
                    session.add(cftc)
                else:
                    session.query(CrawlCftc).filter(CrawlCftc.id == query[0]).update({
                        "net_long": cftc.net_long,
                        "net_short": cftc.net_short
                    })
