import scrapy
from prePushSpider.items import MediaItem
from prePushSpider.configure import media_file
import urlparse
from tldextract import tldextract

class MediaSpider(scrapy.Spider):
    name = 'MediaSpider'
    allowed_domains = ['baidu.com']
    baseUrl = 'www.baidu.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'prePushSpider.pipelines.MediaItemPipeline': 104
        }
    }

    def start_requests(self):
        baseUrl = "http://www.baidu.com/s?"
        for line in open(media_file):
            keyword = baseUrl + 'q1=' + line[0:-1]
            yield scrapy.Request(keyword, callback=self.parse,meta={'name': line[0:-1]})

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        results = sel.xpath('//div[@id="1"]/h3/a/@href').extract()[0]
        yield scrapy.Request(results,callback=self.parse_url,meta = {'name':response.meta['name']})

    def parse_url(self,response):
        mediaItem = MediaItem()
        mediaItem['name'] = response.meta['name']
        #mediaItem['url'] = get_tld(response.url)
        #mediaItem['url'] = urlparse.urlparse(response.url).netloc
        ext = tldextract.extract(response.url)
        if ext.subdomain == 'www':
            mediaItem['url'] = '.'.join(tldextract.extract(response.url)[1:])
        elif ext.domain == 'www':
            mediaItem['url'] = '.'.join(tldextract.extract(response.url)[2:])

        else:
            mediaItem['url'] = '.'.join(tldextract.extract(response.url))
        yield mediaItem


