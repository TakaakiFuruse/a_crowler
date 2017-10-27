
import scrapy
import re


from scrapy.loader import ItemLoader
from rosen_crawler.items import StationItem, RailwayItem
from rosen_crawler.items import StationItemLoader, RailwayItemLoader
from itertools import chain


class AthomeSpider(scrapy.Spider):
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


    name = 'athome'

    def parse(self, response):
        # web_site = scrapy.Field()
        # pref_name = scrapy.Field()
        # railway_company = scrapy.Field()
        # railway = scrapy.Field()
        # bukken_count = scrapy.Field()

        pref_name = re.sub(
            'https://www.athome.co.jp/chintai/(.+)/line/', r"\1", response.url
        )
        # links_to_follow = response.css(
        #     'div.area-group.search-items.limit-ensen.f-fixedTrigger.select-search-cond li label span a::attr(href)').extract()
        railway_names = response.css(
            'div.area-group.search-items.limit-ensen.f-fixedTrigger.select-search-cond li label span a::text').extract()
        bukken_counts = response.css(
            'div.area-group.search-items.limit-ensen.f-fixedTrigger.select-search-cond li label::text').extract()

        attr_list = list(zip(railway_names, bukken_counts))
        for attr in attr_list:
            item_loader = RailwayItemLoader(item=RailwayItem())
            item_loader.add_value('web_site', 'AtHome賃貸')
            item_loader.add_value('pref_name', pref_name)
            item_loader.add_value('railway', attr[0])
            item_loader.add_value('bukken_count', attr[1])
            yield item_loader.load_item()