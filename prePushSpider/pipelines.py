# -*- coding: utf-8 -*-

# Define your item pipelines here


import json
import codecs
import datetime
import time
import os
import Levenshtein
from prePushSpider.configure import KanDianItemFile, site_set, site_filter_flag, site_file, threshold,DownloadDir,ScoreDir
from rss_crawler.MysqlConfig import mysql_cfg

# 解决datetime json序列化问题
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
        f = codecs.open(DownloadDir+'/%s.json'%item['articleId'],'a',encoding ='utf-8')
        line = json.dumps(dict(item),cls=CJsonEncoder)+ '\n'
        f.write(line)
        f.close()
        return item

    def close_spider(self, spider):
        print("crawl finish,start analyze")
        db = mysql_cfg.get_cfg_db_conn()
        f = open(ScoreDir+time.strftime('/score_%Y_%m_%d_%H_%M_%S.txt',time.localtime()),'w')
        print("save log"+ScoreDir+time.strftime('/score_%Y_%m_%d_%H_%M_%S.txt',time.localtime()))
        for i in open(KanDianItemFile):
            article = json.loads(i)
            if article['title'] == u'deleted':
                continue
            sContent = article['content']
            for j in open(DownloadDir+'/%s.json'%article['articleId']):
                dContent = json.loads(j)
                if not self.urlFilter(dContent['baseUrl']):
                    continue
                score = Levenshtein.jaro(sContent, dContent['content'])
                if score < threshold:
                    continue
                db.insertOrUpdate(table="PrePushArticleSource", data={'ArticleID': article['articleId'],
                                                                      'SourceUrl': dContent['url'],
                                                                      'Similarity': score, })
                line = "%s %s %s\n"% (article['articleId'],dContent['url'],score)
                f.write(line)
        f.close()
        db.commit()
        mysql_cfg.disconnect_db(db)
        self.deleteFiles()
        print("analyze finish")

    def urlFilter(self, url):
        if site_filter_flag:
            for site in site_set:
                if url.find(site) != -1:
                    return True
            return False
        else:
            return True

    
    def deleteFiles(self):
        filelist = os.listdir(DownloadDir)
        for f in filelist:
            os.remove(DownloadDir+'/'+f)

class KanDianArticleItemPipeline(object):
    # 看点文章item处理，保存到json
    def __init__(self):
        self.file = codecs.open(KanDianItemFile,'wb',encoding='utf-8')

    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item

    def close_spider(self,spider):
        self.file.close()


class MediaItemPipeline(object):
    def __init__(self):
        self.file = codecs.open(site_file, 'wb', encoding='utf-8')
        self.count = 0

    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        self.count += 1
        return item

    def close_spider(self,spider):
        self.file.close()
        print('爬取'+ str(self.count)+'个网址')
