# -*- coding: utf-8 -*-
from model.crawl_economic_calendar import CrawlEconomicCalendar
from model.crawl_economic_event import CrawlEconomicEvent
from model.crawl_economic_holiday import CrawlEconomicHoliday
from Controller import Controller
import json, requests, logging
from sqlalchemy import and_, or_, func

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/jin10_calendar.log',
                filemode='w')

class Jin10calendardeleteController(Controller):
    def __init__(self, topic="crawl_jin10_calendar_delete"):
        super(Jin10calendardeleteController, self).__init__(topic)
        # self.post_sn_url = 'http://www.9dfx.com/api/content'

        self.update_data = {
            'category': '财经日历',
            'token': self.token,
            'status': -1,
            'tpl': 1,
            'todo': 0,
        }

    def run(self):
        for msg in self.consumer:
            try:
                print msg.value
                data = json.loads(msg.value.decode('utf-8'))
                dtype= data['dtype'] if "dtype" in data else "calendar"

                del data['dtype']
                if len(data['dataname_ids']) > 0:
                    if dtype == 'calendar':
                        self.parse_calendar(data)
                    elif dtype == 'event':
                        self.parse_event(data)
                    elif dtype == 'holiday':
                        self.parse_holiday(data)
            except Exception as e:
                logging.error(e.message)

    def parse_calendar(self, data):
        with self.session_scope(self.sess) as session:
            query = session.query(CrawlEconomicCalendar.fx_id).filter(
                and_(
                    CrawlEconomicCalendar.pub_time.between(data['date'] + '00:00:00', data['date'] + '23:59:59'),
                    ~CrawlEconomicCalendar.source_id.in_(data['dataname_ids'])
                )
            ).all()

            print "calendar", query
            if query and len(query) > 0:
                for id in query:
                    post_data = {}
                    post_data.update(self.update_data)
                    post_data['id'] = id

                    session.query(CrawlEconomicCalendar).filter(and_(
                        CrawlEconomicCalendar.pub_time.between(data['date'] + '00:00:00', data['date'] + '23:59:59'),
                        CrawlEconomicCalendar.fx_id == id
                    )).delete(synchronize_session=False)

    def parse_event(self, data):
        with self.session_scope(self.sess) as session:
            query = session.query(CrawlEconomicEvent.fx_id).filter(
                and_(
                    CrawlEconomicEvent.date == data['date'],
                    ~CrawlEconomicEvent.source_id.in_(data['dataname_ids'])
                )
            ).all()

            print "event", query
            if query and len(query) > 0:
                for id in query:
                    post_data = {}
                    post_data.update(self.update_data)
                    post_data['id'] = id
                    post_data['category'] = '财经大事'

                    session.query(CrawlEconomicEvent).filter(and_(
                        CrawlEconomicEvent.date == data['date'],
                        CrawlEconomicEvent.fx_id == id
                    )).delete(synchronize_session=False)


    def parse_holiday(self, data):
        with self.session_scope(self.sess) as session:
            query = session.query(CrawlEconomicHoliday.fx_id).filter(
                and_(
                    CrawlEconomicHoliday.date == data['date'],
                    ~CrawlEconomicHoliday.source_id.in_(data['dataname_ids'])
                )
            ).all()

            print "holiday", query
            if query and len(query) > 0:
                for id in query:
                    post_data = {}
                    post_data.update(self.update_data)
                    post_data['id'] = id
                    post_data['category'] = '假期休市'

                    session.query(CrawlEconomicHoliday).filter(and_(
                        CrawlEconomicHoliday.date == data['date'],
                        CrawlEconomicHoliday.fx_id == id
                    )).delete(synchronize_session=False)