# -*- coding: utf-8 -*-
from qsbk.items import QsbkItem
import scrapy


class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        duzidivs = response.xpath("//div[@id='content-left']/div")
        for  duzidiv in duzidivs:
            author = duzidiv.xpath(".//h2/text()").extract_first()
            author = author.strip()
            content = duzidiv.xpath(".//div[@class='content']//text()").extract()
            content = "".join(content).strip()
            # import ipdb as pd ; pd.set_trace()
            item = QsbkItem(author=author,content=content)
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").extract_first()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain + next_url,callback=self.parse)
