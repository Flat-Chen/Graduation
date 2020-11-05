# -*- coding: utf-8 -*-
# 字符集编码未UTF-8

# 爬虫项目名字
BOT_NAME = 'guazi'

# 爬虫所在位置 在guazi问价夹的spiders文件夹里面
SPIDER_MODULES = ['guazi.spiders']
NEWSPIDER_MODULE = 'guazi.spiders'

# Obey robots.txt rules
# 是否遵循robotstxt协议，不遵循就是什么网站都爬，遵循就是别人网站告诉你哪里你不能爬 你就不能爬 君子协议
ROBOTSTXT_OBEY = False

# 设置爬取延迟，理论上越快越容易被发现
DOWNLOAD_DELAY = 0

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 爬虫并发数，同时请求的数量，并发越多越吃配置
CONCURRENT_REQUESTS = 16

# Disable cookies (enabled by default)
# 是否允许cookie
COOKIES_ENABLED = True

# Override the default request headers:
# 设置头文件
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# 打开下载中间件 详见上面官方参考文档 下面同理
DOWNLOADER_MIDDLEWARES = {
    'guazi.middlewares.GuaziUserAgentMiddleware': 200,
    'guazi.middlewares.GuaziProxyMiddleware': 100,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 打开存储管道，爬取到数据按照pipline定义的存储规则存储
ITEM_PIPELINES = {
    # 存mysql或者mongo数据库
    # 'guazi.pipelines.GuaziPipeline': 300,
    # 存excel
    'guazi.pipelines.ExcelPipeline': 300,
}

# 是否开启重试
RETRY_ENABLED = True
# 遇到哪些状态码重试
RETRY_HTTP_CODES = [400, 403, 404, 408]
# 重试次数
RETRY_TIMES = 3

# mysql服务器地址
MYSQL_SERVER = '81.68.214.148'
# mysql服务器用户名
MYSQL_USER = "root"
# mysql密码
MYSQL_PWD = "1999"
# mysql端口号
MYSQL_PORT = 3306
# mysql数据库
MYSQL_DB = "guazi"
# MYSQL_TABLE = "guazi_car"

# mongo数据库地址
MONGODB_SERVER = '81.68.214.148'
# mongo数据库库名
MONGODB_DB = 'guazi'
