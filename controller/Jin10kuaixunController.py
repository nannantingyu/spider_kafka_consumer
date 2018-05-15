# -*- coding: utf-8 -*-
from model.crawl_jin10_kuaixun import CrawlJin10Kuaixun
from Controller import Controller
import json, requests, re, logging

class Jin10kuaixunController(Controller):
    def __init__(self, topic="crawl_jin10_kuaixun"):
        super(Jin10kuaixunController, self).__init__(topic, 'jin10_kuaixun')

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                key = data['key']
                del data['dtype']
                del data['key']

                kuaixun = CrawlJin10Kuaixun(**data)
                if '金十' in kuaixun.body or 'jin10' in kuaixun.body or 'jin10' in kuaixun.more_link:
                    continue

                with self.session_scope(self.sess) as session:
                    query = session.query(CrawlJin10Kuaixun.id).filter(
                        getattr(CrawlJin10Kuaixun, key) == getattr(kuaixun, key)
                    ).one_or_none()

                    print query
                    if query is None:
                        session.add(kuaixun)
                        session.flush()
                        data['id'] = kuaixun.id
                        data['dtype'] = "insert"
                        data['source_site'] = "jin10"
                        self.hook_data(data, "kuaixun")
                    else:
                        session.query(CrawlJin10Kuaixun).filter(
                            CrawlJin10Kuaixun.id == query[0]
                        ).update(data)

                        data['id'] = query[0]
                        data['dtype'] = "update"
                        data['source_site'] = "jin10"
                        self.hook_data(data, "kuaixun")
            except Exception, e:
                self.logger.error('Catch an exception.', exc_info=True)