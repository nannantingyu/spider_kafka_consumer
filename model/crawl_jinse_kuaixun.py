# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, SmallInteger, DECIMAL, Date
from model.util import Base

class CrawlJinseKuaixun(Base):
    __tablename__ = 'crawl_jinse_kuaixun'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer)
    live_id = Column(Integer)
    content = Column(String(1024))
    source = Column(String(32))
    publish_time = Column(DateTime)
    source_url = Column(String(256))
    type = Column(SmallInteger)
    website = Column(String(32))
    status = Column(SmallInteger)
    grade = Column(SmallInteger)
    image = Column(String(512))
    link = Column(String(512))
    link_name = Column(String(32))

    created_time = Column(DateTime, default=func.now())
    updated_time = Column(DateTime, default=func.now(), onupdate=func.now())