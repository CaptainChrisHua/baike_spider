# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

# useful for handling different item types with a single interface

from baike_spider.orm.baike_model import BaikeDo
from utils import db, logger, redis_util


class UtcSpiderPipeline:
    def process_item(self, item, spider):
        return item


class BaikePipeline:
    def process_item(self, item, spider):
        obj = BaikeDo(
            topic_id=item.get('topic_id'),
            topic=item.get('topic'),
            category=item.get('category'),
            source=item.get('source'),
            text=item.get('text')
        )
        db.session.add(obj)
        try:
            db.session.flush()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            if hasattr(e, 'orig'):
                if e.orig.args[0] == 1062:
                    redis_util.incr("total_duplicate")
        return item
