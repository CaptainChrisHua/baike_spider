# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UtcSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    topic_id = scrapy.Field()
    topic = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    text = scrapy.Field()


class BaikeItem(scrapy.Item):
    # baike field
    topic_id = scrapy.Field()
    topic = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    text = scrapy.Field()
