FROM python:3.9.12-slim-buster

MAINTAINER xxx

ENV LANG=C.UTF-8

RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt /root/project/baike_spider/requirements.txt

RUN mkdir -p /root/baike_spider/logs && \
pip3 install --no-cache -r /root/project/baike_spider/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /root/project/baike_spider
WORKDIR /root/project/baike_spider

ENV PYTHONPATH=/root/project/baike_spider

CMD scrapy runspider /root/project/baike_spider/baike_spider/spiders/baike_crawl.py
