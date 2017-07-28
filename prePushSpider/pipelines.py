# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import datetime
import Levenshtein
from prePushSpider.configure import *

#解决datetime json无法序列化问题
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y年%m月%d日 %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y年%m月%d日')
        else:
            return json.JSONEncoder.default(self, obj)


class UrlItemPipeline(object):

    def process_item(self, item, spider):
        jsonfile = codecs.open('downloadArticle/%s.json'%item['articleId'],'a',encoding ='utf-8')
        line = json.dumps(dict(item),cls=CJsonEncoder)+ '\n'
        line = line.decode("unicode_escape")
        #jsonfile.write(line.encode('latin-1').decode('unicode_escape'))       #python3
        jsonfile.write(line)      #python2
        jsonfile.close()
        return item

    def close_spider(self,spider):
        for i in open(KanDianItemFile):
            article = json.loads(i)
            if article['title'] == u'deleted':
                continue
            sContent = article['content']
            f = codecs.open('score/%s.json'%article['articleId'],'a',encoding = 'utf-8')
            for j in open('downloadArticle/%s.json'%article['articleId']):
                dContent = json.loads(j)
                score = Levenshtein.jaro(sContent,dContent['content'])
                line = json.dumps({'url': dContent['url'],
                                   'score': score})+'\n'
                f.write(line)
            f.close()


class KanDianArticleItemPipeline(object):
    # 看点文章item处理，保存到json
    def __init__(self):
        self.file = codecs.open('KanDianArticle.json','wb',encoding='utf-8')

    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + '\n'
        line = line.decode("unicode_escape")
        self.file.write(line)
        return item

    def close_spider(self,spider):
        self.file.close()


class MediaItemPipeline(object):
    def __init__(self):
        self.file = codecs.open('url.txt', 'wb', encoding='utf-8')

    def process_item(self,item,spider):
        self.file.write(item['url']+'\n')
        return item

    def close_spider(self,spider):
        self.file.close()

