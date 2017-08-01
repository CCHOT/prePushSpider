# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlItem(scrapy.Item):
    articleId = scrapy.Field()      # cms中文章id
    keyword = scrapy.Field()        # 搜索关键字
    url = scrapy.Field()            # 搜索结果url
    baseUrl = scrapy.Field()        # 搜索结果baseUrl
    desc = scrapy.Field()           # 搜索结果页摘要
    title = scrapy.Field()          # 搜索结果文章标题
    date = scrapy.Field()           # 搜索结果文章时间
    content = scrapy.Field()        # 搜索结果文章内容
    author = scrapy.Field()         # 搜索结果文章作者


class KanDianArticleItem(scrapy.Item):
    url = scrapy.Field()            # cms中文章url
    articleId = scrapy.Field()      # cms中文章id
    date = scrapy.Field()           # cms中文章日期
    author = scrapy.Field()         # cms中文章作者（公众号）
    content = scrapy.Field()        # cms中文章内容
    title = scrapy.Field()          # cms中文章标题


class MediaItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
