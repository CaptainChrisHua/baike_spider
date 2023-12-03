import os
import re
import time
from urllib.parse import unquote

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from baike_spider.items import BaikeItem
from utils import logger, redis_util


# from baike_spider.items import BaikeItem


class BaikeCrawlSpider(CrawlSpider):
    name = "baike_crawl"
    allowed_domains = ["baike.baidu.com"]
    start_url = os.getenv("START_URL")
    if not start_url:
        start_url = redis_util.redis_conn.lpop("url_list")
    start_urls = [start_url]
    rules = (Rule(LinkExtractor(allow=r"/item/([^/]+)/(\d+)"), callback="parse_item", follow=True),)
    # proxy_url = ("https://tps.kdlapi.com/api/gettps/?secret_id=oeb8i6leie0jh4v5xrda&num=1&signature="
    #              "geq17eb8oexuttfmk7bomw1j36t3x5gc&pt=2&sep=1")
    # proxy_ip = requests.get(proxy_url).text
    # username = "17501689688"
    # password = "3238978a"
    # proxies = {
    #     "http": "socks5h://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    #     "https": "socks5h://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
    # }
    count = 0
    total = 0
    start_time = time.time()

    def parse_item(self, response):
        self.total += 1
        match = re.search(r"/item/([^/]+)/(\d+)", response.url)
        try:
            topic = unquote(match.group(1))
            topic_id = match.group(2)
        except AttributeError:
            return
        raw_summary = response.xpath('//div[contains(@class, "J-summary")]//text()').extract()
        cleaned_summary = [re.sub(r' \[\d+\]|\[\d+\]|\n|\xa0', '', item) for item in raw_summary]
        summary = ''.join(cleaned_summary)
        if summary:
            item = BaikeItem()
            item["topic"] = topic
            item["topic_id"] = topic_id
            item["text"] = summary
            item["source"] = "baike"
            yield item
            self.count += 1
            if self.count % 100 == 0:
                redis_util.redis_conn.incrby("topics_number", 100)
                time_used = int(time.time() - self.start_time)
                self.start_time = time.time()
                redis_util.redis_conn.incrby("total_time", time_used)
                total_topics = int(redis_util.redis_conn.get("topics_number"))
                total_time_used = int(redis_util.redis_conn.get("total_time"))
                total_duplicate = int(redis_util.redis_conn.get("total_duplicate"))
                logger.info(
                    f"{self.total}:已爬取{total_topics}条数据，用时{total_time_used // 60}分{total_time_used % 60}秒")
                logger.info(f"累计重复{total_duplicate}条，重复率：{(total_duplicate * 100 / total_topics):.2f}%")
