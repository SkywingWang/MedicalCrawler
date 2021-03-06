import scrapy
from medicalCrawler.items import MedicalcrawlerItem
import sys
import logging
import json
import codecs
import mysql.connector


class MedicalSpider(scrapy.Spider):
    name = 'medicalCrawler'
    allowed_domains = ['db.yaozh.com']
    base_url = 'https://db.yaozh.com/policies/'
    offset = 0
    conn = mysql.connector.connect(host='localhost', user='root', password='root', database='medical')
    sourceUrl = []


    #offset 为偏移量 每次加1
    # offset = 24473
    start_urls = ['https://db.yaozh.com//policies/11517.html']

    # 获取logger实例，如果参数为空则返回root logger
    logger = logging.getLogger("MedicalSpider")
    failure_logger = logging.getLogger("FailureUrl")

    # 文件日志
    file_handler = logging.FileHandler("MesdicalSpider.log")
    failure_handler = logging.FileHandler("FailureUrl.log")

    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_handler.setFormatter(formatter)
    failure_handler.setFormatter(formatter)

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    failure_logger.addHandler(failure_handler)
    def __init__(self):
        self.file = codecs.open('medical.json', 'w', encoding='utf-8')
        # cursor = self.conn.cursor()
        # selectSQL = "select id,url,repeat_times from source_url where request_result = 0 and repeat_times < 5"
        # cursor.execute(selectSQL)
        # self.sourceUrl = cursor.fetchall()
        # startUrl = self.sourceUrl[0][1].replace('\'', '')
        # self.logger.info(startUrl)
        # self.start_urls = [startUrl]
        # cursor.close()



    def parse(self, response):
        medical = MedicalcrawlerItem()
        htmlTitle = response.xpath("//div[@class='manual']/div[@class='title']/text()").extract_first()

        #如果没有获取title认定为空网页
        if(htmlTitle):
            medical['title'] = str(htmlTitle).strip()
            medical['url'] = response.url
            self.logger.info("repsonse url: " + response.url)
            medical['htmlBody'] = response.body.decode(encoding='UTF-8', errors='strict')
            htmlContextList = response.xpath("//div[@class='manual']/div//text()").extract()
            htmlContext = []
            for htmlContextItem in htmlContextList:
                htmlContext.append(str(htmlContextItem).strip())
                htmlContext.append("\n")
            medical['htmlContext'] = "".join(htmlContext)
            headList = response.xpath("//div[@class='manual']/div[@class='content' or @class='content hbg']")

            #获取头部区域的列表中的每条内容，根据span判断  内容所属类别
            for headItem in headList:
                headItemSpan = headItem.xpath("./span/text()").extract_first()
                if(headItemSpan):
                    headItemContext = str(headItem.xpath("string(.)").extract_first())

                    if headItemSpan.find('发布部门')>=0:
                        if (headItemContext.index("】") > 0):
                            headItemContext = headItemContext[headItemContext.index("】") + 1:]
                            headItemContext = headItemContext.strip()
                        medical['releaseDepartment'] = headItemContext
                        self.logger.info("releaseDepartment: " + medical['releaseDepartment'])
                    if headItemSpan.find('效力级别')>=0:
                        if (headItemContext.index("】") > 0):
                            headItemContext = headItemContext[headItemContext.index("】") + 1:]
                            headItemContext = headItemContext.strip()
                        medical['effectivenessLevel'] = headItemContext
                        self.logger.info("effectivenessLevel: " + medical['effectivenessLevel'])
                    if headItemSpan.find('发布日期')>=0:
                        if (headItemContext.index("】") > 0):
                            headItemContext = headItemContext[headItemContext.index("】") + 1:]
                            headItemContext = headItemContext.strip()
                        medical['releaseDate'] = headItemContext
                        self.logger.info("releaseDate: " + medical['releaseDate'])

            tagAList = response.xpath("//div[@class='manual']//a")

            downloaderList = []
            if(tagAList):
                for tagAItem in tagAList:
                    downloaderDic = {}
                    tagAContext = tagAItem.xpath("string(.)").extract_first()
                    downloaderDic['context'] = tagAContext
                    tagAHref = tagAItem.xpath('@href').extract_first()
                    downloaderDic['href'] = tagAHref
                    downloaderList.append(downloaderDic)
            medical['downloaderLinkList'] = downloaderList
            medical['ids'] = self.offset
            # cursorSuccessful = self.conn.cursor()
            # updateSuccessfulSQL = 'UPDATE source_url SET request_result = %s,repeat_times = %s where id = %s;'
            # insertData = [1,self.sourceUrl[self.offset][2] + 1,self.sourceUrl[self.offset][0]]
            # cursorSuccessful.execute(updateSuccessfulSQL,insertData)
            # self.conn.commit()
            # cursorSuccessful.close()
            yield medical
        else:
            thisUrl = self.base_url + str(self.offset) + '.html'
            self.failure_logger.info("failureUrl : " + thisUrl);
            cursorFault = self.conn.cursor()
            updateSuccessfulSQL = 'UPDATE source_url SET request_result = %s,repeat_times = %s where id = %s;'
            insertData = [0, self.sourceUrl[self.offset][2] + 1, self.sourceUrl[self.offset][0]]
            cursorFault.execute(updateSuccessfulSQL, insertData)
            self.conn.commit()
            cursorFault.close()

        # if(self.offset < len(self.sourceUrl)):
        #     self.offset += 1
        #     currentUrl = self.sourceUrl[self.offset][1]
        #     currentUrl = currentUrl.replace('\'', '')
        #     self.logger.info('currentUrl : ' + currentUrl)
        #     yield scrapy.Request(currentUrl, callback=self.parse)
