# -*- coding:utf-8 -*-

import functools
import time

from baike_spider.settings import TIMER
from utils import logger


def timer(unit=None):
    def _timer(func):
        """计时器"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            if TIMER:
                time_used = round(time.time() - start, 3)
                if unit == "ms":
                    logger.info(f'执行函数{func.__name__}，耗时{time_used * 1000}毫秒')
                else:
                    logger.info(f'执行函数{func.__name__}，耗时{time_used}秒')
            return res

        return wrapper

    return _timer
