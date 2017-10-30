# -*- coding: utf-8 -*-

import scrapy
import re

from scrapy.loader import ItemLoader
from rosen_crawler.items import StationItem, RailwayItem
from rosen_crawler.items import StationItemLoader, RailwayItemLoader


class ChintaiRailwaySpider(scrapy.Spider):
    name = 'chintai_railway'
    start_urls = ['https://www.chintai.net/ensen/']

    def parse(self, response):
        railway_links = response.css('a.area__link::attr(href)').extract()

        for link in railway_links:
            yield response.follow(link, self.parse_railway)

    def parse_railway(self, response):
        railway_table_boxes = response.css(
            'section.mod_tableBox.js_check.js_data_tab_content')
        pref_name = re.sub(
            'https://www.chintai.net/(.+)/ensen/', r"\1", response.url
        )
        for box in railway_table_boxes:
            railway_company_name = box.css(
                'div.head div.title h5::text').extract()
            railway_names_and_counts = box.css(
                'div.search_listTable span.txt')

            for name_and_count in railway_names_and_counts:
                railway_name = name_and_count.css('span.name::text').extract()
                count = name_and_count.css('span.num::text').extract()

                item_loader = RailwayItemLoader(item=RailwayItem())
                item_loader.add_value('web_site', 'チンタイ')
                item_loader.add_value('pref_name', pref_name)
                item_loader.add_value('railway_company', railway_company_name)
                item_loader.add_value('railway', railway_name)
                item_loader.add_value('bukken_count', count)
                yield item_loader.load_item()
