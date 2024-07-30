# -*- coding:utf-8 -*-
from baike_spider.settings import SQLALCHEMY_CONFIG, LOG_PATH, LOG_LEVEL, REDIS_CONFIG, MONGODB_CONFIG
from utils.log_utils import LogUtil
from utils.mongo_util import MongoUtil
from utils.mysql_util import SQLAlchemyUtil
from utils.redis_util import RedisUtil

# db = SQLAlchemyUtil(SQLALCHEMY_CONFIG)

logger = LogUtil(log_path=LOG_PATH, log_level=LOG_LEVEL)
redis_util = RedisUtil(REDIS_CONFIG)
mongo = MongoUtil(MONGODB_CONFIG)
