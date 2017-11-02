import scrapy
import re
import time

from scrapy.loader import ItemLoader
from rosen_crawler.items import HomesRailwayItem, HomesRailwayItemLoader
from itertools import chain
from scrapy.utils.markup import remove_tags
from scrapy.shell import inspect_response


class HomesRailwaySpider(scrapy.Spider):
    name = 'homes_railway'
    prefs = {'aomori': '青森県', 'hokkaido': '北海道', 'iwate': '岩手県',
             'miyagi': '宮城県', 'akita': '秋田県', 'yamagata': '山形県',
             'fukushima': '福島県', 'ibaraki': '茨城県', 'tochigi': '栃木県',
             'gunma': '群馬県', 'saitama': '埼玉県', 'chiba': '千葉県', 'tokyo': '東京都',
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
        f'https://www.homes.co.jp/{pref}/line/' for pref in prefs.keys()
    ]

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "rosen_crawler.selenium_middleware.SeleniumMiddleware": 0,
        },
    }

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.homes.co.jp',
            callback=self.fake_request,
        )

        yield scrapy.Request(
            url='https://www.homes.co.jp/chintai/tokyo/line/',
            callback=self.fake_request,
        )

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )

    def fake_request(self, response):
        pass

    def parse(self, response):
        if re.match('https://www.homes.co.jp/distil.+', response.url):
            time.sleep(5)
            yield scrapy.Request(
                url=response.request.meta['redirect_urls'][0],
                callback=self.parse,
                dont_filter=True
            )
        else:
            railway_boxes = response.css(
                'div.mod-checkList.rosen.fitting fieldset')

            for railway_box in railway_boxes:
                railway_company = remove_tags(
                    railway_box.css('legend').extract_first()
                )

                names_and_counts = railway_box.css('ul li label')

                for name_and_count in names_and_counts:
                    bukken_count = remove_tags(
                        name_and_count.css('span').extract_first()
                    )

                    railway_url = name_and_count.css(
                        'a::attr(href)'
                    ).extract_first()

                    railway_name = name_and_count.extract()
                    railway_name = remove_tags(railway_name)
                    railway_name = re.sub('\n|\s', '', railway_name)
                    if railway_name is None:
                        railway_name = 'no_bukken'

                    pref_name = re.sub(
                        'https://www.homes.co.jp/(.+)/line/$', r"\1",
                        response.url
                    )

                    item_loader = HomesRailwayItemLoader(
                        item=HomesRailwayItem()
                    )

                    item_loader.add_value('web_site', 'HOMES')
                    item_loader.add_value('pref_name', self.prefs[pref_name])
                    item_loader.add_value('railway_company', railway_company)
                    item_loader.add_value('railway', railway_name)
                    item_loader.add_value('bukken_count', bukken_count)
                    item_loader.add_value('url', railway_url)
                    yield item_loader.load_item()
