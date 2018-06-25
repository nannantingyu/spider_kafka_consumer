# -*- coding: utf-8 -*-
from model.crawl_jinse_kuaixun import CrawlJinseKuaixun
from Controller import Controller
import json, re, requests, logging, datetime, time
from sqlalchemy import and_, or_, func

class JinsekuaixunController(Controller):
    def __init__(self, topic="crawl_jinse_kuaixun"):
        super(JinsekuaixunController, self).__init__(topic, 'jinse_kuaixun')

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                print data['live_id']
                jinseKuaixun = CrawlJinseKuaixun(**data)
                with self.session_scope(self.sess) as session:
                    query = session.query(CrawlJinseKuaixun.id).filter(and_(
                        CrawlJinseKuaixun.live_id == data['live_id']
                    )).one_or_none()

                    if query is None:
                        print 'add data'
                        session.add(jinseKuaixun)
                        session.flush()
                        data['id'] = jinseKuaixun.id
                        data['dtype'] = "insert"
                        data['source_site'] = "jinse"
                        self.hook_data(data)
                    else:
                        session.query(CrawlJinseKuaixun)\
                            .filter(CrawlJinseKuaixun.live_id == data['live_id'])\
                            .update(data)

                        data['id'] = query.id
                        data['dtype'] = "update"
                        data['source_site'] = "jinse"
                        self.hook_data(data)
            except:
                self.logger.error('Catch an exception.', exc_info=True)
                continue