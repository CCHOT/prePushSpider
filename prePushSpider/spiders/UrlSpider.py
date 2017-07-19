# -*- coding: utf-8 -*-
import scrapy


class UrlSpider(scrapy.Spider):
    name = 'UrlSpider'
    allowed_domains = ['baidu.com']
    

    def parse(self, response):
        pass
