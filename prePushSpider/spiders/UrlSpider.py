# -*- coding: utf-8 -*-
import scrapy
import json
import re
import datetime
from scrapy.utils.response import get_base_url
from prePushSpider.items import UrlItem
from prePushSpider.configure import site_search_flag,site_set,max_page,KanDianItemFile
from newspaper import Article


class UrlSpider(scrapy.Spider):
    name = 'UrlSpider'
    allowed_domains = ['baidu.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'prePushSpider.pipelines.UrlItemPipeline': 103
        }
    }   # 指定urlItem 处理pipeline

    def start_requests(self):
        baseUrl = "http://www.baidu.com/s?"
        for line in open(KanDianItemFile):
            article = json.loads(line)
            if article['title'] == u'deleted':
                continue
            if site_search_flag:
                keyword = baseUrl+'q1=%s'%article['title']                          # 构建baidu搜索url，添加搜索关键字
                for i in site_set:
                    queryUrl = keyword+'&q6='+i
                    # meta参数是为了能够在request之间进行参数传递，与parse中response.meta对应
                    yield scrapy.Request(queryUrl, callback=self.parse,
                                         meta={'articleId': article['articleId'], 'keyword': article['title'], 'page': 0})
            else:
                queryUrl = baseUrl + 'q1=%s' % article['title']
                yield scrapy.Request(queryUrl, callback=self.parse,
                                     meta={'articleId': article['articleId'], 'keyword': article['title'], 'page': 0})

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        results = sel.xpath('//div[@class="result c-container "]')
        page = response.meta['page']
        for result in results:
            urlItem = UrlItem()
            urlItem['keyword'] = response.meta['keyword']
            urlItem['articleId'] = response.meta['articleId']
            urlItem['desc'] = re.sub("[\s+\.\!\/_,\\\\$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）\n]+".decode("utf8"), "".decode("utf8"),
                                     result.xpath('.//div[@class="c-abstract"]').xpath('string(.)').extract()[0])
            # 过滤部分标点
            urlItem['url'] = result.xpath('.//div[@class="f13"]/a/@href').extract()[0]
            # 通过百度搜索页面摘要获取日期
            urlItem['date'] = []
            tt = re.findall(u'^[1-n]+(?:天|小时|分钟)[前内]', urlItem['desc'])
            for i in tt:
                sub = re.findall(u'(^[1-n])+天前', i)
                if not sub:     # 今天的日期
                    urlItem['date'].append(datetime.date.today())
                for j in sub:   # 以前的日期
                    urlItem['date'].append(datetime.date.today() - datetime.timedelta(days=int(j)))
            tt1 = re.findall(u'^(?:19|20)\d\d年(?:1[012]|0?[1-9])月(?:(?:[12][0-9])|(?:3[01])|(?:(?:0?)[1-9]))日', urlItem['desc'])
            for i in tt1:
                urlItem['date'].append(i)
            yield scrapy.Request(urlItem['url'], meta={'urlItem': urlItem}, callback=self.parse_url)

        if page < max_page-1:
            try:
                nextUrl = sel.xpath(u'//a[contains(.,"下一页")]').xpath(u'./@href').extract()[0]
                yield scrapy.Request(response.urljoin(nextUrl), callback=self.parse,
                                     meta={'page': page+1,'articleId':urlItem['articleId'],'keyword':urlItem['keyword']})
            except:
                pass

    def parse_url(self,response):
        urlItem = response.meta['urlItem']
        urlItem['url'] = response.url           # 重定项后
        urlItem['baseUrl'] = get_base_url(response)

        # newspaper
        article = Article(url='', language='zh')
        article.set_html(response.text)
        article.parse()
        urlItem['title'] = re.sub("[\s+\.\!\/_,\\\\\$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）\n]+".decode("utf8"),
                                  "".decode("utf8"), article.title)
        urlItem['content'] = re.sub("[\s+\.\!\/_,\\\\\$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）\n]+".decode("utf8"),
                                    "".decode("utf8"), article.text)
        urlItem['author'] = article.authors         # 基本提取不到
        yield urlItem

