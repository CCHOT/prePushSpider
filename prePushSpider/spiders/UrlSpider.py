# -*- coding: utf-8 -*-
import scrapy
import json
import re
import logging
from prePushSpider.items import UrlItem
#from readability import Document
from newspaper import Article,fulltext
from scrapy.utils.url import urlparse


class UrlSpider(scrapy.Spider):
    name = 'UrlSpider'
    allowed_domains = ['baidu.com']
    baseUrl = 'www.baidu.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'prePushSpider.pipelines.UrlItemPipeline': 103
        }
    }   # 指定urlItem 处理pipeline

    def start_requests(self):
        for line in open("KanDianArticle.json",encoding='utf-8'):   #python3
        #for line in open("KanDianArticle.json"):                   #python2
            article = json.loads(line)
            # 构建baidu搜索url，设置callback函数，
            # meta参数是为了能够在request之间进行参数传递，与parse中response.meta对应
            yield scrapy.Request("http://www.baidu.com/s?wd=%s"%article['title'],callback=self.parse,
                                 meta={'articleId':article['articleId'],'keyword':article['title'],'page':0})

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        results =sel.xpath('//div[@class="result c-container "]')
        page = response.meta['page']
        for result in results:
            urlItem = UrlItem()
            try:
                urlItem['keyword'] = response.meta['keyword']
                urlItem['articleId'] = response.meta['articleId']
                urlItem['desc'] = result.xpath('.//div[@class="c-abstract"]').xpath('string(.)').extract()[0]
                urlItem['url'] = result.xpath('.//div[@class="f13"]/a/@href').extract()[0]
                yield scrapy.Request(urlItem['url'],meta={'urlItem':urlItem},callback=self.parse_url)
            except:
                pass

        if page < 2:
            try:
                nextUrl = sel.xpath(u'//a[contains(.,"下一页")]').xpath(u'./@href').extract()[0]
                yield scrapy.Request(response.urljoin(nextUrl), callback=self.parse,
                                     meta={'page': page+1,'articleId':urlItem['articleId'],'keyword':urlItem['keyword']})
            except:
                pass
        else:
            pass

    def parse_url(self,response):
        urlItem = response.meta['urlItem']
        urlItem['url'] = response.url           # 重定项后

        #doc = Document(response.text)
        #urlItem['title'] = doc.short_title()
        #urlItem['content'] = re.sub('<[^<]+?>', '', doc.summary())

        article = Article(url='',language='zh')
        article.set_html(response.text)
        article.parse()

        #article = Article(urlItem['url'],language='zh')
        try:
            #article.download()
            #article.parse()
            urlItem['title'] = article.title
            urlItem['content'] = article.text
            urlItem['author'] = article.authors
            urlItem['date'] = article.publish_date
            yield urlItem
        except:
            pass



