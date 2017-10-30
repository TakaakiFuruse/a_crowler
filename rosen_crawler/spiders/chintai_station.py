# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.loader import ItemLoader
from rosen_crawler.items import StationItem, RailwayItem
from rosen_crawler.items import StationItemLoader, RailwayItemLoader
from scrapy.shell import inspect_response


class SearchUrlGenerator(object):
    """docstring for SearchUrlGenerator"""

    def __call__(self, values_list, pref_name):
        return [f"https://www.chintai.net/select/?action=eki&prefKey={pref_name}&e={value}" for value in values_list]


search_url_generator = SearchUrlGenerator()


class ChintaiStationSpider(scrapy.Spider):
    name = 'chintai_station'
    start_urls = ['https://www.chintai.net/ensen/']
    web_site_name = 'チンタイ'

    def parse(self, response):
        railway_links = response.css('a.area__link::attr(href)').extract()

        for link in railway_links:
            yield response.follow(link, self.parse_railway)

    def parse_railway(self, response):
        railway_table_boxes = response.css(
            'section.mod_tableBox.js_check.js_data_tab_content'
        )
        pref_name = re.sub(
            'https://www.chintai.net/(.+)/ensen/', r"\1", response.url
        )
        for box in railway_table_boxes:
            query_values = box.css(
                'input::attr(value)'
            ).extract()

            station_urls = search_url_generator(query_values, pref_name)

            for station_url in station_urls:
                yield response.follow(station_url, self.parse_station)

    def parse_station(self, response):
        railway_name = response.css(
            'div.title.title_set h4.title_set_heading::text'
        ).extract()

        station_names = response.css(
            'div.search_listTable span.name::text'
        ).extract()

        pref_name = re.sub(
            'https:\/\/www\.chintai\.net\/select\/\?action=eki&prefKey=([a-z]+)&e=[0-9]+\Z', r"\1", response.url)

        for station_name in station_names:
            item_loader = StationItemLoader(item=StationItem())
            item_loader.add_value('web_site', self.web_site_name)
            item_loader.add_value('pref_name', pref_name)
            item_loader.add_value('railway', railway_name)
            item_loader.add_value('station', station_name)
            yield item_loader.load_item()
