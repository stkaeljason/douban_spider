# -*- coding: utf-8 -*-
import scrapy
from jason_spider.items import JasonSpiderItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import sys, re, requests, json, random


reload(sys)
sys.setdefaultencoding('utf-8')



class DabSpider(CrawlSpider):
    base_url = 'http://api.douban.com/v2/movie/search?tag='
    tag_list = [
        '爱情']



    name = "doubanmovie"
    start_urls = [(base_url + t +'&start=' + str(i)) for t in tag_list for i in xrange(37820, 40020, 20)]
    def parse(self, response):
        print response.url
        item = JasonSpiderItem()
        r = json.loads(response.body)
        data = r['subjects']
        if data:
            for i in data:
                item['movie_entity'] = i
                yield item
