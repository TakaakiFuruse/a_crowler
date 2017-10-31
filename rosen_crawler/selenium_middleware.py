# -*- coding: utf-8 -*-

from scrapy.http import HtmlResponse
from selenium import webdriver


firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

driver = webdriver.Firefox(firefox_profile=firefox_profile)

class SeleniumMiddleware(object):

    def process_request(self, request, spider):
        driver.get(request.url)

        return HtmlResponse(driver.current_url,
                            body=driver.page_source,
                            encoding='utf-8',
                            request=request)
