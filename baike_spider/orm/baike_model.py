# -*- coding: UTF-8 -*
__author__ = 'chris'

from sqlalchemy import Column, Integer, String, Text

from baike_spider.orm import BaseDao


class BaikeDo(BaseDao):
    """
    DAO class
    """
    __tablename__ = 'baike'

    topic = Column(String(255), comment='topic')
    topic_id = Column(Integer, nullable=False, comment='topic_id')
    category = Column(String(32), comment='category')
    source = Column(String(32), nullable=False, default='baike', comment='source')
    text = Column(Text, comment='text')
