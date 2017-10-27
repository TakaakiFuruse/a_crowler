# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity

class StationItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    web_site = scrapy.Field()
    pref = scrapy.Field()
    railway_company = scrapy.Field()
    railway = scrapy.Field()
    station = scrapy.Field()
