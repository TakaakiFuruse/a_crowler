
import scrapy
import re

from scrapy_splash import SplashRequest

from scrapy.loader import ItemLoader
from rosen_crawler.items import StationItem, RailwayItem
from rosen_crawler.items import StationItemLoader, RailwayItemLoader
from itertools import chain
from scrapy.utils.markup import remove_tags
from random import shuffle
from xml.dom import minidom


class HomesStationSpider(scrapy.Spider):

    name = 'homes_station'

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "rosen_crawler.selenium_middleware.SeleniumMiddleware": 0,
        },
    }

    def start_requests(self):
        a_sitemap = open('./homes-sitemap-chintai-rosen.xml')
        an_xml = minidom.parse(a_sitemap)
        urls = [
            elm.childNodes[0].data for elm in an_xml.getElementsByTagName('loc')
        ]
        shuffle(urls)
        yield scrapy.Request(
            url='https://www.homes.co.jp/',
            callback=self.fake_request
        )
        yield scrapy.Request(
            url='https://www.homes.co.jp/chintai/hokkaido/city/',
            callback=self.fake_request
        )
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def fake_request(self, response):
        pass

    def parse(self, response):
        print(response.body)

        enabled_stations = response.css(
            'ul.checkboxLinkList li label span a::text'
        ).extract()
        disabled_stations = response.css(
            'ul.checkboxLinkList li.disabled label span.linkName::text'
        ).extract()

        railway_name = response.css('span.linkNameAll').extract_first()

        pref_name = re.sub(
            'https://www.homes.co.jp/chintai/(.+)/.+/$', r"\1", response.url
        )

        stations = enabled_stations + disabled_stations

        for station_name in stations:
            item_loader = StationItemLoader(item=StationItem())
            item_loader.add_value('web_site', 'AtHome賃貸')
            item_loader.add_value('pref_name', pref_name)
            item_loader.add_value('railway', remove_tags(railway_name))
            item_loader.add_value('station', remove_tags(station_name))
            yield item_loader.load_item()
