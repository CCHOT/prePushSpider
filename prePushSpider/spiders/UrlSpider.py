# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import logging

class UrlSpider(scrapy.Spider):
    name = 'UrlSpider'
    allowed_domains = ['baidu.com']

    def start_requests(self):

        for article in articles:
            logging.debug("spider url:%s" %article["title"])
            yield scrapy.Request("https://www.baidu.com/s?wd=%s" %article["title"],self.parse)

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        urls =sel.xpath('//*/div[@class="f13"]/a/href')
        for url in urls:
            logging.debug("before url:%s" %url)
            yield Request(url, callback=self.parse_url)

    def parse_url(self,response):
        logging.debug("after url:%s",str(response.url))



