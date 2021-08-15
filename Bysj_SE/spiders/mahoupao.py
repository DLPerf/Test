import scrapy


class MahoupaoSpider(scrapy.Spider):
    name = 'mahoupao'
    allowed_domains = ['bbs.mahoupao.com/']
    start_urls = ['http://bbs.mahoupao.com//']

    def parse(self, response):
        pass
