# -*- coding: utf-8 -*-
import scrapy
import logging
from prePushSpider.items import KanDianArticleItem
import pandas as pd


class KanDianArticleSpider(scrapy.Spider):
    name = "KanDianArticleSpider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'prePushSpider.pipelines.KanDianArticleItemPipeline': 400
        }
    }

    articleId = ""

    def start_requests(self):
        articleInfo = pd.read_csv('D:\\prePushSpider\\select_test.csv', header=0, sep='\t')
        urls = articleInfo["ContentURL"]
        articleIds = articleInfo["ArticleID"]
        for url in urls:
            #self.articleId = articleIds[i]
            yield scrapy.Request(url,self.parse)

    def parse(self,response):
        sel = scrapy.selector.Selector(response)
        kanDianArticleItem = KanDianArticleItem()
        #kanDianArticleItem['articleId'] = self.articleId
        kanDianArticleItem['url'] = str(response.url)
        kanDianArticleItem['title'] = sel.xpath('//*[@id="activity-name"]/text()').extract()
        kanDianArticleItem['date'] = sel.xpath('//*[@id="account_top"]/div[2]/em[1]/text()').extract()
        kanDianArticleItem['author'] = sel.xpath('//*[@id="account_top"]/div[1]/div/text()').extract()
        kanDianArticleItem['content'] = sel.xpath('//*[@id="js_content"]').xpath('string(.)').extract()[0]
        logging("aaaaaaaaaaaaa")
        yield kanDianArticleItem

