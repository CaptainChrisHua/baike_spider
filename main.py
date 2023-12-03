# -*- coding:utf-8 -*-
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "runspider", "baike_spider/spiders/baike_crawl.py"])
