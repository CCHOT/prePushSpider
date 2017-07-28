# -*- coding: utf-8 -*-
import scrapy
import json
import re
import logging
import datetime
from prePushSpider.items import UrlItem
from prePushSpider.configure import *
from readability import Document
from newspaper import Article,fulltext
from goose import Goose


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
        # for line in open(KanDianItemFile,encoding='utf-8'):     #python3
        for line in open(KanDianItemFile):                              #python2
            article = json.loads(line)
            if article['title'] == u'deleted':
                continue
            keyword = baseUrl+'q1=%s'%article['title']                          # 构建baidu搜索url，添加搜索关键字
            for i in site_set:
                queryUrl = keyword+'&q6='+i
                # meta参数是为了能够在request之间进行参数传递，与parse中response.meta对应
                yield scrapy.Request(queryUrl, callback=self.parse,
                                     meta={'articleId': article['articleId'], 'keyword': article['title'],'page': 0})

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        results =sel.xpath('//div[@class="result c-container "]')
        page = response.meta['page']
        for result in results:
            urlItem = UrlItem()
            try:
                urlItem['keyword'] = response.meta['keyword']
                urlItem['articleId'] = response.meta['articleId']
                urlItem['desc'] = re.sub("[\s+\.\!\/_,\\\\$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）\n]+".decode("utf8"),"".decode("utf8"),
                                         result.xpath('.//div[@class="c-abstract"]').xpath('string(.)').extract()[0])
                urlItem['url'] = result.xpath('.//div[@class="f13"]/a/@href').extract()[0]
                # 通过百度搜索页面摘要获取日期
                urlItem['date'] = []
                tt = re.findall(u'^[1-n]+(?:天|小时|分钟)[前内]', urlItem['desc'])
                for i in tt:
                    sub = re.findall(u'(^[1-n])+天前', i)
                    if not sub:
                        urlItem['date'].append(datetime.date.today())
                    for j in sub:
                        urlItem['date'].append(datetime.date.today() - datetime.timedelta(days=int(j)))
                tt1 = re.findall(u'^(?:19|20)\d\d年(?:1[012]|0?[1-9])月(?:(?:[12][0-9])|(?:3[01])|(?:(?:0?)[1-9]))日',
                                 urlItem['desc'])
                for i in tt1:
                    urlItem['date'].append(i)
                yield scrapy.Request(urlItem['url'],meta={'urlItem':urlItem},callback=self.parse_url)
            except:
                pass

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

        # readability-lxml
        # doc = Document(response.text)
        # urlItem['title'] = doc.short_title()
        # urlItem['content'] = re.sub('<[^<]+?>', '', doc.summary())

        # 通过html，正则表达式过滤获取日期。对于也面不干净的，包含多个日期的无法判断准确的日期
        """
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', response.text)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        urlItem['date'] = re.findall(u'(?:19|20)\d\d(?:-|(?: )+|年)(?:1[012]|0?[1-9])(?:-|(?: )+|月)(?:(?:[12][0-9])|(?:3[01])|(?:(?:0?)[1-9]))(?:(?: +)|日)?',s)
        """

        # newspaper
        # article = Article(urlItem['url'],language='zh')
        article = Article(url='', language='zh')
        article.set_html(response.text)
        #article.download()
        article.parse()
        urlItem['title'] = re.sub("[\s+\.\!\/_,\\\\\$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）\n]+".decode("utf8"),
                                               "".decode("utf8"), article.title)
        urlItem['content'] = re.sub("[\s+\.\!\/_,\\\\\$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）\n]+".decode("utf8"),
                                               "".decode("utf8"), article.text)
        urlItem['author'] = article.authors         # 基本提取不到
        # urlItem['date'] = article.publish_date    # 基本提取不到

        # goose
        # g = Goose()
        # article = g.extract(urlItem['url'])
        # urlItem['content'] = article.cleaned_text
        # urlItem['title'] = article.title
        # urlItem['author'] = article.authors
        yield urlItem

