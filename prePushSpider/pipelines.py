# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import datetime

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
        line = json.dumps(dict(item),cls=CJsonEncoder)+'\n'
        #jsonfile.write(line.encode('latin-1').decode('unicode_escape'))       #python3
        jsonfile.write(line.decode("unicode_escape"))      #python2
        jsonfile.close()
        return item


class KanDianArticleItemPipeline(object):
    # 看点文章item处理，保存到json
    def __init__(self):
        self.file = codecs.open('KanDianArticle.json','wb',encoding='utf-8')

    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        return item
