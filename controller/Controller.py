# -*- coding: utf-8 -*-
import sys, os, logging, datetime
reload(sys)
sys.setdefaultencoding("utf-8")
from kafka import KafkaConsumer
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from model.util import db_connect, create_news_table
import settings
import requests
import threading

@contextmanager
def session_scope(session):
    sess = session()
    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        sess.close()

class Controller(object):
    def __init__(self, topic, name):
        engine = db_connect()
        create_news_table(engine)
        self.sess = sessionmaker(bind=engine)
        self.server = settings.kafka
        self.session_scope = session_scope
        self.token = '9286168e06a110cd374caa0f67f08199'
        self.name = name

        log_dir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d"))
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        self.logger = logging.getLogger()
        handler = logging.FileHandler(filename=os.path.join(log_dir, "%s.log"%name))
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)

        if topic:
            self.consumer = KafkaConsumer(topic, bootstrap_servers=self.server['host'], group_id='spider_consumer_client')

    def hook_data(self, data, data_formatter=None):
        self.logger.info('[Hook Data]: %s' % data_formatter)
        data_formatter = settings.data_formatter[data_formatter] if data_formatter is not None else settings.data_formatter[self.name]
        post_data = {}
        for key in data_formatter['data_format']:
            key_to = data_formatter['data_format'][key]
            if key in data:
                post_data[key_to] = data[key]

        for url in data_formatter['post_url_lists']:
            t = threading.Thread(target=self.start_post_data, args=(url, post_data))
            t.start()
            # self.start_post_data(url, post_data)


    def start_post_data(self, url, post_data):
        try:
            r = requests.post(url, data=post_data)
            self.logger.info('[result] %s ' % r.text)
        except Exception, e:
            self.logger.error("[Post error %s]" % url, exc_info=True)
        finally:
            self.logger.info("[Post to %s]" % url)