# -*- coding: utf-8 -*-

# Scrapy settings for prePushSpider project
#
BOT_NAME = 'prePushSpider'
SPIDER_MODULES = ['prePushSpider.spiders']
NEWSPIDER_MODULE = 'prePushSpider.spiders'
ROBOTSTXT_OBEY = False

# 代理设置
DOWNLOADER_MIDDLEWARES = {
    'prePushSpider.middlewares.ProxyMiddleware': 101,
}


