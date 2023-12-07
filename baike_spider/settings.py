# Scrapy settings for baike_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "baike_spider"

SPIDER_MODULES = ["baike_spider.spiders"]
NEWSPIDER_MODULE = "baike_spider.spiders"

LOG_FILE = "/root/logs/baike/all.log"
LOG_LEVEL = "INFO"
LOG_PATH = "/root/logs/baike"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "baike_spider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "baike_spider.middlewares.UtcSpiderSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "baike_spider.middlewares.RandomUserAgent": 43,
    # 'baike_spider.middlewares.ProxyDownloaderMiddleware': 100
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "baike_spider.pipelines.BaikePipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

SQLALCHEMY_CONFIG = {
    'host': '43.132.152.169',
    'port': 3306,
    'database': 'baike',
    'username': 'chris',
    'password': 'chris',
    "charset": "utf8mb4",  # 字符类型
    "pool_size": 10,  # 连接池size
    "max_overflow": 10,  # 超过连接池最大连接数
    "pool_recycle": 60,  # 60s回收一次连接
    "autoflush": False,  # 自动刷新(事务过程中刷新数据)
    "autocommit": False,  # 自动提交事务
    "connect_timeout": 10,  # 连接超时10s
    "echo": False  # 打印sql语句
}

REDIS_CONFIG = {
    'host': '43.132.152.169',
    'port': '6666',
    'db': '6',
    'password': 'chris'
}
#
# SQLALCHEMY_CONFIG = {
#    'host': '101.34.249.241',
#    'port': 3308,
#    'database': 'baike',
#    'username': 'root',
#    'password': 'chris',
#    "charset": "utf8mb4",  # 字符类型
#    "pool_size": 10,  # 连接池size
#    "max_overflow": 10,  # 超过连接池最大连接数
#    "pool_recycle": 60,  # 60s回收一次连接
#    "autoflush": False,  # 自动刷新(事务过程中刷新数据)
#    "autocommit": False,  # 自动提交事务
#    "connect_timeout": 10,  # 连接超时10s
#    "echo": False  # 打印sql语句
# }
#
# REDIS_CONFIG = {
#    'host': '101.34.249.241',
#    'port': '6666',
#    'db': '6',
#    'password': 'chris'
# }