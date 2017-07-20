# -*- coding: utf-8 -*-
import scrapy
import logging
from prePushSpider.items import KanDianArticleItem
import pandas as pd

class KanDianArticleSpider(scrapy.Spider):
    name = "KanDianArticleSpider"

    custom_settings = {
        'ITEM_PIPELINES':{
            'prePushSpider.pipelines.KanDianArticleItemPipeline':1,
        }
    }

    def start_requests(self):
        articleInfo = pd.read_csv('D:\\prePushSpider\\select_test.csv', header=0, sep='\t')
        urls = articleInfo["ContentURL"]
        articleId = articleInfo["ArticleID"]
        articleTitle = articleInfo["Subject"]
        for url in urls:
            logging.debug("spider url:%s" %url)
            yield scrapy.Request(url,self.parse)

    def parse(self,response):
        sel = scrapy.selector.Selector(response)
        kanDianArticleItem = KanDianArticleItem()
        kanDianArticleItem['url'] = str(response.url)
        kanDianArticleItem['title'] = sel.xpath('//*[@id="activity-name"]/text()').extract()
        kanDianArticleItem['date'] = sel.xpath('//*[@id="account_top"]/div[2]/em[1]/text()').extract()
        kanDianArticleItem['author'] = sel.xpath('//*[@id="account_top"]/div[1]/div/text()').extract()
        contentDiv = sel.xpath('//*[@id="js_content"]')
        kanDianArticleItem['content'] = contentDiv.xpath('string(.)').extract()[0]

        yield kanDianArticleItem
