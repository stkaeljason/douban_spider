# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from jason_spider.items import JasonSpiderItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider,Spider
import json
import sys


reload(sys)
sys.setdefaultencoding('utf-8')



class DabSpider(CrawlSpider):
    name = "normalspider"
    start_urls = ['http://music.163.com/#/discover/artist']

    driver = webdriver.PhantomJS()

    def parse(self, response):
        self.driver.get(response.url)
        html = self.driver.page_source
        self.driver.quit()

        print html
        print type(html)

        sel = Selector(text=html)
        title = sel.xpath('//').extract()[0]
        print title
