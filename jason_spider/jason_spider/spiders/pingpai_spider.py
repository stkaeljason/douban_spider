# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from jason_spider.items import JasonSpiderItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor
import json
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


class DabSpider(CrawlSpider):
    name = "jiadian"
    start_urls = ['http://price.ea3w.com/pinpai/']
    rules = [
        Rule(LinkExtractor(allow=('(^"/pinpai/subcate")'), restrict_xpaths='//dd/a[@class="more"]'), callback='parse_pinpai_cate', follow=False)

    ]

    def parse_pinpai_cate(self, response):
        sel = Selector(response)
