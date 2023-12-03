# -*- coding:utf-8 -*-
import logging
import os
import pathlib
import sys
from logging import StreamHandler, Formatter
from logging.handlers import WatchedFileHandler


class LogUtil(logging.Logger):

    logging_name_to_Level = {
        'CRITICAL': logging.CRITICAL,
        'FATAL': logging.FATAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
    }

    def __init__(self, log_path, log_level, name='mylogger'):
        super(LogUtil, self).__init__(name)

        # 创建日志目录，从环境变量LOG_PATH获取日志目录，没有就使用log_path参数值
        log_path = pathlib.Path(os.environ.get("LOG_PATH") or log_path)
        if not log_path.exists():
            log_path.mkdir(parents=True)

        # 设置日志级别
        self.setLevel(self.logging_name_to_Level.get(log_level.upper(), logging.INFO))

        # 日志格式：[时间]-[日志级别]-[文件名-行号]-[信息]-[进程PID]-[线程号]
        _format = '%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] %(message)s - %(process)d-%(thread)d'

        # 添加日志Handler
        default_handlers = {
            WatchedFileHandler(os.path.join(log_path, 'all.log')): logging.INFO,  # INFO日志写入all.log文件
            WatchedFileHandler(os.path.join(log_path, 'error.log')): logging.ERROR,  # ERROR日志写入error.log文件
            StreamHandler(sys.stdout): logging.DEBUG,  # 控制台输出DEBUG信息
            StreamHandler(sys.stderr): logging.ERROR   # 控制台输出ERROR信息
        }
        for handler, level in default_handlers.items():
            handler.setFormatter(Formatter(_format))
            if level is not None:
                handler.setLevel(level)
            self.addHandler(handler)
