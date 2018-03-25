# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import os
import requests
import logging
import sys
import pdfkit

class MedicalcrawlerPipeline(object):

    # 获取logger实例，如果参数为空则返回root logger
    logger = logging.getLogger("MedicalcrawlerPipeline")

    # 文件日志
    file_handler = logging.FileHandler("MedicalcrawlerPipeline.log")

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_handler.setFormatter(formatter)

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    def __init__(self):
        self.ids = set()
        self.rootPath = './medicalResult'

    def open_spider(self,spider):
        if(not os.path.exists(self.rootPath)):
            os.mkdir(self.rootPath)
    def process_item(self, item, spider):

        if item['ids'] in self.ids:
            raise DropItem("Duplicate item found %s" & item['url'])
        else:
            self.ids.add(item['ids'])
            title = item['title'].replace('/', '_')
            title = title.replace('《', '_').replace('》', '_').replace("、", '_').replace("（", '_').replace("）", "_")
            releaseDate = item['releaseDate'].replace('/', '_')
            if len(title) > 30:
                title = title[0:30]
            thePath = os.path.join(self.rootPath, item['releaseDepartment'],item['effectivenessLevel'],releaseDate+'_'+ title)
            if(not os.path.exists(thePath)):
                os.makedirs(thePath)
            filePath = os.path.join(thePath, releaseDate +'_'+ title +'.txt')
            try:
                contextFile = open(filePath, "w")
                contextFile.write(item['htmlContext'])
            except IOError:
                self.logger.error('contextFile Error:', IOError)
            finally:
                contextFile.close()
            htmlPath = os.path.join(thePath,releaseDate+'_'+ title +'.html')
            try:
                htmlFile = open(htmlPath,"w")
                htmlFile.write(item['htmlBody'])
            except IOError:
                self.logger.error('htmlFile Error:', IOError)
            finally:
                htmlFile.close()

            #生成PDF
            pdfPath = os.path.join(thePath,releaseDate+'_'+ title +'.pdf')
            options = {
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'custom-header': [
                    ('Accept-Encoding', 'gzip')
                ],
                'cookie': [
                    ('cookie-name1', 'cookie-value1'),
                    ('cookie-name2', 'cookie-value2'),
                ],
                'outline-depth': 20,
                'zoom': 3,
            }

            pdfkit.from_string(item['htmlContext'], pdfPath, options=options)

            if(item['downloaderLinkList']):
                for downloaderLink in item['downloaderLinkList']:
                    req = requests.get(downloaderLink['href'],stream=True)
                    if(downloaderLink['context'].find('/') > 0):
                        continue
                    try:
                        linkPath = os.path.join(thePath,downloaderLink['context'])
                        self.logger.info(linkPath)
                        linkFile = open(linkPath,'wb')
                        for chunk in req.iter_content(chunk_size=1024):
                            if(chunk):
                                linkFile.write(chunk)
                    except IOError:
                        self.logger.error('linkFile Error:', IOError)

                linkFile.close()
        return item



