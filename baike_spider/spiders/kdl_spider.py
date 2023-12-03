# -*- coding:utf-8 -*-
import scrapy


class KdlSpider(scrapy.spiders.Spider):
    name = "kdl"

    def start_requests(self):
        url = ("https://tps.kdlapi.com/api/gettps/?secret_id=oeb8i6leie0jh4v5xrd"
               "a&num=1&signature=geq17eb8oexuttfmk7bomw1j36t3x5gc&pt=2&sep=1")
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        print(response.text)
