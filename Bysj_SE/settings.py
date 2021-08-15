# Scrapy settings for Bysj_SE project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'CISearch.settings'

django.setup()

sys.setrecursionlimit(1000000)


BOT_NAME = 'Bysj_SE'


#   爬虫的目录
SPIDER_MODULES = ['Bysj_SE.spiders']
NEWSPIDER_MODULE = 'Bysj_SE.spiders'

# #  连接redis
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
# SCHEDULER_PERSIST = True
#
# REDIS_HOST = "106.52.6.65"
# REDIS_PORT = 6379



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Bysj_SE (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#   最大并发请求数
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#  下载延迟，是默认的最小延迟
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
#  针对某个域名的最大并发
CONCURRENT_REQUESTS_PER_DOMAIN = 100
#  针对某个IP的最大并发
CONCURRENT_REQUESTS_PER_IP = 100

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# COOKIES_DEBUG = TRUE    #  进入调试模式

# Disable Telnet Console (enabled by default)
#  监听当前爬虫的状态
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Bysj_SE.middlewares.BysjSeSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Bysj_SE.middlewares.ProxyMiddleware': 543,
   # 'Bysj_SE.middlewares.RandomUserAgentMiddleware': 543,
   # 'Bysj_SE.middlewares.BysjSeDownloaderMiddleware': 543,

}


# RANDOM_UA_TYPE = "random"

# PROXIES = [
#    "http://223.215.18.61:9999",
#    "http://58.253.153.91:9999",
#    "http://60.169.240.202:9999"
#          ]

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https:/  /docs.scrapy.org/en/latest/topics/item-pipeline.html


#  值小的优先
ITEM_PIPELINES = {
   # 'Bysj_SE.pipelines.BysjSePipeline': 300,
    'Bysj_SE.pipelines.HaichuanPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline':400,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#  使得请求的频率参差不齐，根据网站情况自动调节下载速度
#AUTOTHROTTLE_ENABLED = True
# The initial download delay   第一个请求延迟多少
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies  最大的延迟为多少
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#  关于缓存
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# DEPTH_LIMIT =  20   #在原来的基础上多一层递归。  值为0 的时候是不限制，默认为0
# DUPEFILTER_CLASS = "Bysj_SE.duplication.RepeatFilter"

# 广度优先（1）还是深度优先（0）
# DEPTH_PRIORITY = 0    #  这个值只能是 0 或者 1

# DB = 123


# 是否启用缓存策略
# HTTPCACHE_ENABLED = True

# 缓存策略：所有请求均缓存，下次在请求直接访问原来的缓存即可
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"


# 缓存保存路径
# HTTPCACHE_DIR = 'httpcache'


DATATIME_FORMAT = "%Y-%m-%d"


"""
需要在Setting里面注册的东西：
定义的setting配置变量名必须大写，否则 crawler.setting.get('DB') 获取不到
DEPTH_LIMIT = 1   #在原来的基础上多一层递归。  值为0 的时候是不限制，默认为0

DUPEFILTER_CLASS = "Bysj_SE.duplication.RepeatFilter"

ITEM_PIPELINES = {
   'Bysj_SE.pipelines.BysjSePipeline': 300,
}

"""


