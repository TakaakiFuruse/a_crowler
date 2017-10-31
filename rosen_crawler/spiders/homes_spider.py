import scrapy
import re


from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from rosen_crawler.items import StationItem
from itertools import chain


class HomesSpider(SitemapSpider):
    name = 'homes'
    sitemap_urls = ['https://www.homes.co.jp/sitemap-chintai-rosen.xml']
    sitemap_rules = [(r'/chintai/', 'parse_rosen')]

    def parse_rosen(self, response):
        return scrapy.Request
        print(response)