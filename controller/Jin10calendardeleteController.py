# -*- coding: utf-8 -*-
from model.crawl_economic_calendar import CrawlEconomicCalendar
from model.crawl_economic_event import CrawlEconomicEvent
from model.crawl_economic_holiday import CrawlEconomicHoliday
from Controller import Controller
import json, requests, logging
from sqlalchemy import and_, or_, func

class Jin10calendardeleteController(Controller):
    def __init__(self, topic="crawl_jin10_calendar_delete"):
        super(Jin10calendardeleteController, self).__init__(topic, 'jin10_calendar_delete')

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
                self.logger.error('Catch an exception.', exc_info=True)

    def parse_calendar(self, data):
        with self.session_scope(self.sess) as session:
            query = session.query(CrawlEconomicCalendar.id).filter(
                and_(
                    CrawlEconomicCalendar.pub_time.between(data['date'] + '00:00:00', data['date'] + '23:59:59'),
                    ~CrawlEconomicCalendar.source_id.in_(data['dataname_ids'])
                )
            ).all()

            ids = [x[0] for x in query]

            if ids and len(ids) > 0:
                session.query(CrawlEconomicCalendar).filter(
                    CrawlEconomicCalendar.id.in_(ids)
                ).delete(synchronize_session=False)

                pdata = {
                    "dtype": "delete",
                    "type": "calendar",
                    "source_site": "jin10",
                    "id": ",".join(ids)
                }

                self.hook_data(pdata, 'delete_calendar')

    def parse_event(self, data):
        with self.session_scope(self.sess) as session:
            query = session.query(CrawlEconomicEvent.fx_id).filter(
                and_(
                    ~CrawlEconomicEvent.source_id.in_(data['dataname_ids'])
                )
            ).all()

            ids = [x[0] for x in query]

            if ids and len(ids) > 0:
                session.query(CrawlEconomicEvent).filter(and_(
                    CrawlEconomicEvent.id.in_(ids)
                )).delete(synchronize_session=False)

                pdata = {
                    "dtype": "delete",
                    "type": "event",
                    "source_site": "jin10",
                    "id": ",".join(ids)
                }

                self.hook_data(pdata, 'delete_calendar')

    def parse_holiday(self, data):
        with self.session_scope(self.sess) as session:
            query = session.query(CrawlEconomicHoliday.fx_id).filter(
                and_(
                    CrawlEconomicHoliday.date == data['date'],
                    ~CrawlEconomicHoliday.source_id.in_(data['dataname_ids'])
                )
            ).all()

            ids = [x[0] for x in query]

            if ids and len(ids) > 0:
                session.query(CrawlEconomicHoliday).filter(and_(
                    CrawlEconomicHoliday.id.in_(ids)
                )).delete(synchronize_session=False)

                pdata = {
                    "dtype": "delete",
                    "type": "holiday",
                    "source_site": "jin10",
                    "id": ",".join(ids)
                }

                self.hook_data(pdata, 'delete_calendar')