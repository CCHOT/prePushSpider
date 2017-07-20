# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlItem(scrapy.Item):
    keyword = scrapy.Field()
    url = scrapy.Field()
    desc = scrapy.Field()


class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()


class KanDianArticleItem(scrapy.Item):
    url = scrapy.Field()
    articleId = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()

