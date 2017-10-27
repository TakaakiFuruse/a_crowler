# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity


class RailwayItem(scrapy.Item):
    web_site = scrapy.Field()
    pref_name = scrapy.Field()
    railway_company = scrapy.Field()
    railway = scrapy.Field()
    bukken_count = scrapy.Field()


class RailwayItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = Identity()


class StationItem(scrapy.Item):
    web_site = scrapy.Field()
    pref_name = scrapy.Field()
    railway = scrapy.Field()
    station = scrapy.Field()


class StationItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = Identity()
