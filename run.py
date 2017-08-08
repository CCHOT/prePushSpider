# -*- coding = utf-8 -*-
from twisted.internet import reactor,defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from prePushSpider.spiders.KanDianArticleSpider import KanDianArticleSpider

setting = get_project_settings()
runner = CrawlerRunner(get_project_settings())

# 'followall' is the name of one of the spiders of the project.



@defer.inlineCallbacks
def crawl():
    yield runner.crawl(KanDianArticleSpider)
    yield runner.crawl('UrlSpider')
    reactor.stop()

crawl()
reactor.run()

