# -*- coding: utf-8 -*-
import scrapy
from prePushSpider.items import KanDianArticleItem
import pandas as pd

class KanDianArticleSpider(scrapy.Spider):
    name = "KanDianArticleSpider"


    def start_requests(self):
        articleInfo = pd.read_csv('D:\\prePushSpider\\select_test.csv')
        urls = articleInfo["ContentURL"]
        articleId = articleInfo["ArticleId"]
        articleTitle = articleInfo["Subject"]
        for url in urls:
            yield scrapy.Request(url,self.parse)

    def parse(self,response):
        sel = scrapy.selector.Selector(response)
        kanDianArticleItem = KanDianArticleItem()
        kanDianArticleItem['url'] = str(response.url)
        kanDianArticleItem['title'] = sel.xpath()



        pass
