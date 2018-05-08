# -*- coding: utf-8 -*-
from model.crawl_stock import CrawlStock
from Controller import Controller
import json, re, requests, logging
from sqlalchemy import and_, or_, func

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/article.log',
                filemode='w')

class StockController(Controller):
    def __init__(self, topic="crawl_stock"):
        super(StockController, self).__init__(topic)

    def run(self):
        for msg in self.consumer:
            data = json.loads(msg.value.decode('utf-8'))
            stock = CrawlStock(**data)
            with self.session_scope(self.sess) as session:
                if stock.type == 3:
                    query = session.query(CrawlStock.id).filter(
                        and_(
                            CrawlStock.type == stock.type,
                            CrawlStock.position == stock.position,
                            CrawlStock.publish_time == stock.publish_time
                        )
                    ).one_or_none()
                else:
                    query = session.query(CrawlStock.id).filter(
                        and_(
                            CrawlStock.type == stock.type,
                            CrawlStock.publish_time == stock.publish_time
                        )
                    ).one_or_none()

                if query is None:
                    session.add(stock)
                else:
                    session.query(CrawlStock).filter(CrawlStock.id == query[0]).update({
                        "position": stock.position,
                        "iod": stock.iod
                    })