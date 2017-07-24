# -*- coding: utf-8 -*-
import scrapy
import logging
import pandas as pd
from prePushSpider.items import KanDianArticleItem



class KanDianArticleSpider(scrapy.Spider):
    name = "KanDianArticleSpider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'prePushSpider.pipelines.KanDianArticleItemPipeline': 102
        }
    }           # 指定该spider返回item处理的pipeline

    def start_requests(self):
        articleInfo = pd.read_csv('D:\\prePushSpider\\select_test.csv', header=0, sep='\t')
        urls = articleInfo["ContentURL"]
        articleIds = articleInfo["ArticleID"]
        for i in xrange(len(urls)):
            # 创建Request，设置callback函数,
            # meta参数是为了能够在request之间进行参数传递，与parse中response.meta对应
            yield scrapy.Request(urls[i],meta={'articleId':articleIds[i]},callback=self.parse)

    # 起始url爬虫
    def parse(self,response):
        sel = scrapy.selector.Selector(response)
        kanDianArticleItem = KanDianArticleItem()
        kanDianArticleItem['url'] = response.url        # 防止重定向url
        kanDianArticleItem['title'] = sel.xpath('//*[@id="activity-name"]/text()').extract()[0]
        kanDianArticleItem['date'] = sel.xpath('//*[@id="account_top"]/div[2]/em[1]/text()').extract()[0]
        kanDianArticleItem['author'] = sel.xpath('//*[@id="account_top"]/div[1]/div/text()').extract()[0]
        kanDianArticleItem['content'] = sel.xpath('//*[@id="js_content"]').xpath('string(.)').extract()[0]
        kanDianArticleItem['articleId'] = str(response.meta['articleId'])
        yield kanDianArticleItem