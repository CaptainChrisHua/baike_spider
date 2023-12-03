# -*- coding:utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import declarative_base


class BaseModel(object):
    id = Column(BIGINT(unsigned=True), primary_key=True, nullable=False, doc='')


BaseDao = declarative_base(cls=BaseModel)
