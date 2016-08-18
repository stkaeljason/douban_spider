# -*- coding: utf-8 -*-
import scrapy
from jason_spider.items import JasonSpiderItem
from scrapy.selector import Selector
from scrapy.http import Request


class ForeignUniversity(scrapy.Spider):
    name = "France_university"
    start_urls = ['http://www.jsj.edu.cn/n1/12033.shtml']

    def parse(self, response):
        item = JasonSpiderItem()
        selector = Selector(response)
        universities = selector.xpath('//div[@class="gwList"]')
        for uni in universities:
            item['name'] = uni.xpath('p[2]/text()').extract()[0].lstrip(u'中文校名：').strip()
            item['concept'] = u"国外大学"
            item['en_name'] = uni.xpath('p[1]/text()').extract()[0].lstrip(u'法文校名：').strip()
            item['location'] = u'法国'
            yield item