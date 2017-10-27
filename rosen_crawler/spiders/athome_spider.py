
import scrapy
import re


from scrapy.loader import ItemLoader
from rosen_crawler.items import StationItem
from itertools import chain


class AtHomeSpider(scrapy.Spider):
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
        f'https://www.athome.co.jp/chintai/{pref}/line/'for pref in prefs.index()
    ]
    name = 'athome'

    def parse_rosen(self, response):
        return scrapy.Request
        print(response)
