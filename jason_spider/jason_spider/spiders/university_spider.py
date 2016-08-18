# -*- coding: utf-8 -*-
__author__ = 'jason'
import scrapy,  urllib, re
from scrapy.selector import Selector
from scrapy.http import Request, HtmlResponse
#from Universities.items import UniversitiesItem
from bs4 import BeautifulSoup


class UniversitySpider(scrapy.Spider):
    name = "university_spider"
    start_urls = ['http://www.ccug.net/fenlei/bxlx11.htm'
                  #'http://www.ccug.net/fenlei/bxlx12.htm'
                  #'http://www.ccug.net/fenlei/bxlx13.htm'
                  #'http://www.ccug.net/fenlei/bxlx14.htm'
                  ]
    base_url = "http://www.ccug.net"

    # 学校独立页面的解析函数
    def parse_single_university(self, response):
        selector = Selector(response)
        item = response.meta['item']
        # 提取校徽url
        badge_url_part = selector.xpath('//img[@height="80"]/@src').extract()
        if badge_url_part:
            badge_url = self.base_url + badge_url_part[0].lstrip('.')
        else:
            badge_url = ''
        # 提取学校英文名称
        en_name = selector.xpath('//table[@align="center"][3]/tr[2]/td[2]/text()').extract()
        if en_name:
            en_name = en_name[0]
        else:
            en_name = ''
        # 提取学校所在城市
        city = selector.xpath('//table[@align="center"][5]/tr[5]/td[2]/a/text()').extract()[0]
        # 提取原始学校等级
        level_origin = selector.xpath('//table[@align="center"][5]/tr[1]/td[2]/a/text()').extract()
        if len(level_origin) > 1:
            level = level_origin[0]
        else:
            level = u"普本"  # 需要根据start_urls的不同url进行手动变化

        item['badge_url'] = badge_url
        item['en_name'] = en_name
        item['city'] = city
        item['level'] = level
        yield item

    # 主解析函数
    def parse(self, response):

        item = UniversitiesItem()
        selector = Selector(response)
        # 检索页面所有的按地域分块的学校集合
        university_groups = selector.xpath('//table[@align="center"]/tr[2]')
        for university_group in university_groups:

            # 对单个集合按行进行检索形成行的学校集合
            university_trs = university_group.xpath('td/table/tr')
            for university_tr in university_trs:
                universities = university_tr.xpath('td/a')
                for university in universities:
                    uni_url = university.xpath('@href').extract()[0]     # 获得单个学校的url片段
                    xuexiao_url = self.base_url + uni_url                    # 拼接总的url

                    # 获取所需网页字段内容
                    name = university.xpath('text()').extract()[0]
                    nickname = ''
                    country = 'china'
                    print name

                    # 放进item对象中
                    item['name'] = name
                    item['nickname'] = nickname
                    item['country'] = country
                    yield Request(xuexiao_url, callback='parse_single_university',
                                  meta={'item': item}, dont_filter=True)     # 记得设置参数dont_filter=True



