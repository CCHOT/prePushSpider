import scrapy
from scrapy.utils.response import get_base_url
from prePushSpider.items import MediaItem

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
        for line in open("media.txt"):
            keyword = baseUrl + 'q1=%s' % line
            yield scrapy.Request(keyword, callback=self.parse)

    def parse(self, response):
        sel = scrapy.selector.Selector(response)
        results = sel.xpath('//div[@id="1"]/h3/a/@href').extract()[0]
        yield scrapy.Request(results,callback=self.parse_url)

    def parse_url(self,response):
        mediaItem = MediaItem()
        mediaItem['url'] = get_base_url(response)
        yield mediaItem


