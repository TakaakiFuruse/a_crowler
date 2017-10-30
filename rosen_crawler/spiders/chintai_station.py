# -*- coding: utf-8 -*-
import scrapy


class ChintaiStationSpider(scrapy.Spider):
    name = 'chintai_station'
    allowed_domains = ['rosen_crawler']
    start_urls = ['http://rosen_crawler/']

    def parse(self, response):
        pass
