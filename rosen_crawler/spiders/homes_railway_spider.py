
import scrapy
import re


from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from rosen_crawler.items import StationItem
from itertools import chain
from scrapy.shell import inspect_response

class HomesRailwaySpider(SitemapSpider):
    sitemap_urls = ['https://www.homes.co.jp/sitemap-chintai-rosen.xml']
    sitemap_rules = [(r'/chintai/', 'parse_rosen')]


    def parse_rosen(self, response):
        inspect_response(response, self)