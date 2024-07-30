# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent

from scrapy import signals

from utils import logger, redis_util

# from settings import PROXY_LIST

ua = UserAgent()


# useful for handling different item types with a single interface


class RandomUserAgent(object):

    def process_request(self, request, spider):
        request.headers['User-Agent'] = ua.random


# class RandomProxy(object):
#
#     def process_request(self, request, spider):
#         proxy  = random.choice(PROXY_LIST)
#         request.headers['User-Agent'] = ua.random


class ProxyDownloaderMiddleware:
    _proxy = ('h104.kdltps.com', '15818')

    def process_request(self, request, spider):
        # 用户名密码认证
        username = "t10191882634024"
        password = "y7jja6hs"
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                                        "proxy": ':'.join(
                                                                            ProxyDownloaderMiddleware._proxy)}
        # 白名单认证
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}

        request.headers["Connection"] = "close"
        return None

    def process_exception(self, request, exception, spider):
        """捕获407异常"""
        if "'status': 407" in exception.__str__():  # 不同版本的exception的写法可能不一样，可以debug出当前版本的exception再修改条件
            from scrapy.resolver import dnscache
            dnscache.__delitem__(ProxyDownloaderMiddleware._proxy[0])  # 删除proxy host的dns缓存
        return exception
