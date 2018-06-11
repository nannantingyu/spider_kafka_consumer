# -*- encoding: utf-8 -*-
"""
定义数据库模型实体 
"""
from sqlalchemy import Column, Integer, SmallInteger, String, Text, DateTime, func, Index
from model.util import Base

class CrawlVipOnline(Base):
    """行情资讯类"""
    __tablename__ = 'crawl_vip_online'

    id = Column(Integer, primary_key=True)
    site1 = Column(String(32))
    logined1 = Column(SmallInteger, nullable=True)
    guest1 = Column(SmallInteger, nullable=True)

    site2 = Column(String(32))
    logined2 = Column(SmallInteger, nullable=True)
    guest2 = Column(SmallInteger, nullable=True)

    site3 = Column(String(32))
    logined3 = Column(SmallInteger, nullable=True)
    guest3 = Column(SmallInteger, nullable=True)

    created_time = Column(DateTime)