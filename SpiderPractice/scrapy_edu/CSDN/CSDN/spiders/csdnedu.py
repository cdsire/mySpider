# -*- coding: utf-8 -*-
import scrapy
import CSDN.items
import urllib.request
import urllib
import lxml.etree
import re

class CsdneduSpider(scrapy.Spider):
    name = 'csdnedu'
    allowed_domains = ['edu.csdn.net']
    start_urls = ['http://edu.csdn.net/lecturer?&page=1']
    offset = 1
    lastpage = 0

    def __init__(self):
        # 类初始化，构造函数
        self.lastpage = self.geturlnumbers(self.start_urls[0])
        # 继承父类
        super().__init__()

    # 获取总页数
    def geturlnumbers(self, url):
        # 获取页面数据
        data = urllib.request.urlopen(url).read().decode("utf-8")
        # 解析页面
        mytree = lxml.etree.HTML(data)
        # 解析页面,抓取元素
        mytext = mytree.xpath("//*[@class=\"text\"][last()]/text()")[1]
        regex = re.compile("\d+", re.IGNORECASE)
        # 获取总数据量
        num = eval(regex.findall(mytext)[0])

        # 计算页数
        pages = 0
        if num % 20 == 0:
            pages = num //20
        else:
            pages = num // 20 + 1
        return pages
    # 解析
    def parse(self, response):
        mytree = response
        nodedata = mytree.xpath("//*[@class=\"panel-body\"]//dl/dd/p/text()").extract()
        nodename = mytree.xpath("//*[@class=\"panel-body\"]//dl/dd/ul//li[1]/a/text()").extract()
        nodelessions = mytree.xpath("//*[@class=\"panel-body\"]//dl/dd/ul//li[2]/span/text()").extract()
        nodestudents = mytree.xpath("//*[@class=\"panel-body\"]//dl/dd/ul//li[3]/span/text()").extract()

        for i in range(len(nodedata)):
            csdnitem = CSDN.items.CsdnItem()
            csdnitem["name"] = nodename[i]
            csdnitem["lessons"] = nodelessions[i]
            csdnitem["students"] = nodestudents[i]
            csdnitem["title"] = nodedata[i]
            yield csdnitem

        if self.offset <= self.lastpage:
            self.offset += 1

        newurl = "http://edu.csdn.net/lecturer?&page="+str(self.offset)
        yield scrapy.Request(newurl, self.parse)    # 翻页，自己调用自己