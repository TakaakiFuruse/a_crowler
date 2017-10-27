
import scrapy
import re
import itertools


from scrapy.loader import ItemLoader
from rosen_crawler.items import StationItem, RailwayItem
from rosen_crawler.items import StationItemLoader, RailwayItemLoader
from scrapy.utils.response import open_in_browser


class AthomeStationSpider(scrapy.Spider):
    prefs = {'hokkaido': '北海道', 'aomori': '青森県', 'iwate': '岩手県',
             'miyagi': '宮城県', 'akita': '秋田県', 'yamagata': '山形県',
             'fukushima': '福島県', 'ibaraki': '茨城県', 'tochigi': '栃木県',
             'gumma': '群馬県', 'saitama': '埼玉県', 'chiba': '千葉県', 'tokyo': '東京都',
             'kanagawa': '神奈川県', 'niigata': '新潟県', 'toyama': '富山県',
             'ishikawa': '石川県', 'fukui': '福井県', 'yamanashi': '山梨県',
             'nagano': '長野県', 'gifu': '岐阜県', 'shizuoka': '静岡県',
             'aichi': '愛知県', 'mie': '三重県', 'shiga': '滋賀県', 'kyoto': '京都府',
             'osaka': '大阪府', 'hyogo': '兵庫県', 'nara': '奈良県',
             'wakayama': '和歌山県', 'tottori': '鳥取県', 'shimane': '島根県',
             'okayama': '岡山県', 'hiroshima': '広島県', 'yamaguchi': '山口県',
             'tokushima': '徳島県', 'kagawa': '香川県', 'ehime': '愛媛県',
             'kochi': '高知県', 'fukuoka': '福岡県', 'saga': '佐賀県',
             'nagasaki': '長崎県', 'kumamoto': '熊本県', 'oita': '大分県',
             'miyazaki': '宮崎県', 'kagoshima': '鹿児島県', 'okinawa': '沖縄県'}

    start_urls = [
        f'https://www.athome.co.jp/chintai/{pref}/line/'for pref in prefs.keys()
    ]

    name = 'athome_station'

    def parse(self, response):

        links_to_follow = response.css(
            'div.area-group.search-items.limit-ensen.f-fixedTrigger.select-search-cond li label span a::attr(href)').extract()
        railway_names = response.css(
            'div.area-group.search-items.limit-ensen.f-fixedTrigger.select-search-cond li label span a::text').extract()
        bukken_counts = response.css(
            'div.area-group.search-items.limit-ensen.f-fixedTrigger.select-search-cond li label::text').extract()

        attr_list = list(itertools.zip_longest(
            railway_names, bukken_counts, links_to_follow))
        for attr in attr_list:
            yield response.follow(attr[2], self.parse_stations)

    def parse_stations(self, response):
        pref_name = re.sub(
            'https://www.athome.co.jp/chintai/(.+)/.+/$', r"\1", response.url
        )

        station_names = response.css('ul#station-list li label span a::text').extract()
        railway =  response.css('#search-station > h2 > label::text').extract()[0]
        for station_name in station_names:
            item_loader = StationItemLoader(item=StationItem())
            item_loader.add_value('web_site', 'AtHome賃貸')
            item_loader.add_value('pref_name', pref_name)
            item_loader.add_value('railway', railway)
            item_loader.add_value('station', station_name)
            yield item_loader.load_item()
