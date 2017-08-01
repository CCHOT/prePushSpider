# -*- coding: utf-8 -*-
# 爬取看点文章

import scrapy
import pandas as pd
import re
from prePushSpider.items import KanDianArticleItem
from prePushSpider.configure import KanDianListFile


class KanDianArticleSpider(scrapy.Spider):
    name = "KanDianArticleSpider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'prePushSpider.pipelines.KanDianArticleItemPipeline': 102
        }
    }           # 指定该spider返回item处理的pipeline

    def start_requests(self):
        articleInfo = pd.read_csv(KanDianListFile, header=0, sep='\t')      # 读取articleId和url
        urls = articleInfo["ContentURL"]
        articleIds = articleInfo["ArticleID"]
        for i in xrange(len(urls)):
            # 创建Request，设置callback函数,
            # meta参数是为了能够在request之间进行参数传递，与parse中response.meta对应
            yield scrapy.Request(urls[i],meta={'articleId':articleIds[i]},callback=self.parse)

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        kanDianArticleItem = KanDianArticleItem()
        kanDianArticleItem['articleId'] = str(response.meta['articleId']).decode('utf-8')
        kanDianArticleItem['url'] = response.url        # 重定向后的url
        try:
            kanDianArticleItem['title'] = sel.xpath('//*[@id="activity-name"]/text()').extract()[0]
            kanDianArticleItem['content'] = sel.xpath('//*[@id="js_content"]').xpath('string(.)').extract()[0]
            kanDianArticleItem['content']= re.sub("[\s+\.\!\/_,\\\\$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）\n]+".decode("utf8"),
                                                  "".decode("utf8"), kanDianArticleItem['content'])
        except:
            kanDianArticleItem['title'] = u'deleted'    # 文章被删除了的情况
            kanDianArticleItem['date'] = u''
            kanDianArticleItem['author'] = u''
            kanDianArticleItem['content'] = u''

        if kanDianArticleItem['title'] != u'deleted':
            try:
                kanDianArticleItem['date'] = sel.xpath('//*[@id="account_top"]/div[2]/em[1]/text()').extract()[0]
                kanDianArticleItem['author'] = sel.xpath('//*[@id="account_top"]/div[1]/div/text()').extract()[0]
            except:
                # 看点文章url中两种日期和作者结构
                kanDianArticleItem['date'] = sel.xpath('//div[@class="rich_media_meta_list account clearfix"]/em[2]/text()').extract()[0]
                kanDianArticleItem['author'] = sel.xpath('//div[@class="rich_media_meta_list account clearfix"]/em[3]/text()').extract()[0]
        yield kanDianArticleItem
