import time
import random

from selenium.webdriver import Chrome

import smtk.utils.logger as l


def random_js_scroll():
    scroll_size = random.randrange(6000, 100000)
    return "window.scrollTo(0, %s)" % (str(scroll_size))

def random_sleep():
    sleep_sec = random.randrange(2, 10)
    time.sleep(sleep_sec)


class GoogleImageCrawler:

    def __init__(self, keywords, scroll_max = 3):
        self.keywords = keywords
        self.scroll_max = scroll_max
        self.page_source = None

    @property
    def search_url_prefix(self):
        return "https://www.google.com.sg/search?q="

    @property
    def search_url_suffix(self):
        return ''.join(['&source=lnms&tbm=isch&sa=X',
                        '&ei=0eZEVbj3IJG5uATalICQAQ&ved=0CAcQ_AUoAQ',
                        '&biw=939&bih=591'])

    def on_start(self, keyword):
        pass

    def on_entry(self, keyword, entry):
        raise RuntimeError('on_entry must be implemented')

    def on_page_source(self):
        raise RuntimeError("on_page_source must be implemented")


    def build_search_url(self, keyword):
        return ''.join([
            self.search_url_prefix,
            keyword,
            self.search_url_suffix])

    def update_page_source(self, keyword):
        url = self.build_search_url(keyword)

        driver = Chrome()
        driver.get(url)


        num_scrolls = 0
        try:

            while num_scrolls < self.scroll_max:
                driver.execute_script(random_js_scroll())
                self.page_source = driver.page_source
                random_sleep()
                num_scrolls+=1

        except Exception as e:
            l.WARN(e)

        driver.close()

    def crawl_keyword(self, keyword):
        self.update_page_source(keyword)
        self.on_page_source()

    def crawl(self):
        for keyword in self.keywords:
            self.on_start(keyword)
            self.crawl_keyword(keyword)

