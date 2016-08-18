# -*- coding: utf-8 -*-
import scrapy
from jason_spider.items import JasonSpiderItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
""" item['entity'] item['concept']  item['label'] item['alias']"""


class DabSpider(CrawlSpider):
    name = "town_village"
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2014/index.html'
                  ]
    # url的遍逆规则最初始的放在最下面
    rules = [
             Rule(LinkExtractor(allow=('(\d+)'), restrict_xpaths=('//tr[@class="towntr"]/td[2]')), callback='parse_village', follow=True),
             Rule(LinkExtractor(allow=('(\d+)'), restrict_xpaths=('//tr[@class="countytr"]/td[2]')), callback='parse_town', follow=True),
             Rule(LinkExtractor(allow=('(\d+)')))
             ]


    def parse_town(self, response):
        print 'ssss'
        sel = Selector(response)
        groups = sel.xpath('//tr[@class="towntr"]')
        for g in groups:
            item = JasonSpiderItem()
            item['entity'] = g.xpath('td[2]/a/text()').extract()[0]
            if u'镇' in item['entity']:
                item['concept'] = u'镇'
            elif u'乡' in item['entity']:
                item['concept'] = u'乡'
            yield item

    def parse_village(self, response):
        villages = response.xpath('//tr[@class="villagetr"]')
        for v in villages:
            item = JasonSpiderItem()
            name = v.xpath('td[3]/text()').extract()[0]
            if u'村' in name:
                point = name.index(u'委会')
                item['entity'] = name[:point]
                item['concept'] = u'村'
                yield item











