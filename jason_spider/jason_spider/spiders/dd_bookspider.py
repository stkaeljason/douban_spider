# -*- coding: utf-8 -*-
import scrapy
from jason_spider.items import JasonSpiderItem
from scrapy.selector import Selector
from scrapy.http import Request
""" item['entity'] item['concept']  item['label'] item['alias']"""



class DabSpider(scrapy.Spider):
    name = "bookspider"
    start_urls = ['http://category.dangdang.com/cp01.00.00.00.00.00.html'
                  ]

    def parse_single_page(self, response):
        base_url = 'http://category.dangdang.com'
        item = JasonSpiderItem()
        selector = Selector(response)
        couns = selector.xpath('//ul[@class="list_aa listimg"]/li')
        for c in couns:

            name = c.xpath('div/p[@class="name"]/a/text()').extract()[0]
            if u'（' in name:
                point = name.index(u'（')
                item['entity'] = name[:point]
            else:
                item['entity'] = name
            author = c.xpath('div/div[1]/p[@class="author"]/a/text()').extract()
            if author:
                item['author'] = author[0]
            # 对概念和标签进行解析判断
            concept = selector.xpath('//div[@class="sort_box"]/h3/text()').extract()[0]
            if concept == u"图书":
                concept = selector.xpath('//div[@class="sort_box"]/ul/li[1]/a/@title').extract()[0]
                item['label'] = selector.xpath('//div[@class="sort_box"]/ul/li[1]/div/span[1]/a/@title').extract()[0]
            else:

                item['label'] = selector.xpath('//div[@class="sort_box"]/ul/li[1]/a/@title').extract()[0]

            if '/' in concept:
                new_concept =concept.replace('/', '')
                item['concept'] = new_concept
            else:
                item['concept'] = concept
            yield item


        next_link = selector.xpath('//li[@class="next"]/a/@href').extract()
        if next_link:
            next_url = base_url + next_link[0]
            yield Request(next_url, callback=self.parse_single_page)


    def parse_label(self, response):
        base_url = 'http://category.dangdang.com'
        selector = Selector(response)
        labels = selector.xpath('//div[@class="sort_box"]/ul/li')
        for lab in labels:
            spans = lab.xpath('div/span')
            #print spans
            for span in spans:
                label_url = span.xpath('a/@href').extract()[0]

                url =base_url + label_url[:label_url.index('#')]
                yield Request(url, callback=self.parse_single_page)

    def parse(self, response):
        base_url = 'http://category.dangdang.com'
        # item = JasonSpiderItem()
        selector = Selector(response)
        concepts = selector.xpath('//div[@class="sort_box"]/ul/li')
        for con in concepts:
            """
            concept = con.xpath('a/text()').extract()[0].strip()
            if '/' in concept:
                new_concept =concept.replace('/', '')
                item['concept'] = new_concept
            else:
                item['concept'] = concept
            """

            concept_url = con.xpath('a/@href').extract()[0]
            new_concept_url = concept_url.replace('.html', '-f0%7C0%7C0%7C0%7C0%7C0%7C0%7C0%7C0%7C0%7C0%7C0.html')
            url = base_url + concept_url[:concept_url.index('#')]
            yield Request(url, callback=self.parse_label)


