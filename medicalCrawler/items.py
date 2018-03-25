# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MedicalcrawlerItem(scrapy.Item):
    # define the fields for your item here like:

    #id  保证item唯一性，以url的页面索引做id
    ids = scrapy.Field()

    #url
    url = scrapy.Field()

    #标题
    title = scrapy.Field()

    #页面全部内容
    htmlBody = scrapy.Field()

    #页面内容
    htmlContext = scrapy.Field()

    #发布部门
    releaseDepartment = scrapy.Field()

    #效力级别
    effectivenessLevel = scrapy.Field()

    #发布日期
    releaseDate = scrapy.Field()

    #下载文件链接列表
    downloaderLinkList = scrapy.Field()

