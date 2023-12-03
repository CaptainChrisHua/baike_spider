# -*- coding:utf-8 -*-
import json
import re
from typing import Any
from urllib.parse import unquote

import scrapy
from scrapy.http import Response
import json


class BaikeSpider(scrapy.Spider):
    name = "baike"
    allowed_domains = ["baike.baidu.com"]
    start_urls = ["https://baike.baidu.com/item/%E9%87%91%E8%9E%8D/860"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        match = re.search(r"/item/([^/]+)/(\d+)", response.url)
        topic = unquote(match.group(1))
        topic_id = match.group(2)
        raw_summary = response.xpath('//div[contains(@class, "J-summary")]//text()').extract()
        cleaned_summary = [re.sub(r' \[\d+\]|\[\d+\]|\n|\xa0', '', item) for item in raw_summary]
        summary = ''.join(cleaned_summary)

        data = {
            "topic": topic,
            "topic_id": topic_id,
            "text": summary
        }
        print(data)
        with open("baike.json", "a") as f:
            f.write(json.dumps(data, ensure_ascii=False))
            f.write("\n")

        # todo 更换ip
        # todo 登录
        # todo 破解转动验证码
