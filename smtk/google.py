import time
import random

import multiprocessing
from queue import Queue

from threading import Thread

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

import smtk.utils.logger as l

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

def scroll_bottom():
    return "window.scrollTo(0, document.body.scrollHeight);"

def random_sleep():
    sleep_sec = random.randrange(2, 10)
    time.sleep(sleep_sec)


class GoogleImageKeywordCrawler():

    def __init__(self, keyword, scroll_max = 3):
        self.keyword = keyword
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

    def on_start(self):
        pass

    def on_entry(self, entry):
        raise RuntimeError('on_entry must be implemented')

    def on_page_source(self):
        raise RuntimeError("on_page_source must be implemented")


    def build_search_url(self):
        return ''.join([
            self.search_url_prefix,
            self.keyword,
            self.search_url_suffix])

    def update_page_source(self):
        l.INFO("""
               Starting page source update, scrolling: %s times
               """ % (self.scroll_max))

        url = self.build_search_url()

        options = ChromeOptions()
        options.add_argument('--user-agent=%s' %(USER_AGENT))
        driver = Chrome(chrome_options=options)
        driver.get(url)


        num_scrolls = 0
        try:

            while num_scrolls < self.scroll_max:
                l.INFO("New Scroll: %s" % (num_scrolls + 1))

                driver.execute_script(scroll_bottom())

                fetch_more_button = (
                    driver
                    .find_element_by_css_selector(".ksb._kvc")
                )

                if fetch_more_button:
                    l.INFO("Fetch More Button Found")
                    driver.execute_script("document.querySelector('.ksb._kvc').click();")
                    driver.execute_script(scroll_bottom())

                self.page_source = driver.page_source
                random_sleep()
                num_scrolls+=1

        except Exception as e:
            l.WARN(e)

        driver.close()

    def crawl_keyword(self):
        self.update_page_source()
        self.on_page_source()

    def crawl(self):
        self.on_start()
        self.crawl_keyword()


class GoogleImageCrawler():

    def __init__(self, task_cls, queue_data, **kwargs):
        self.task_cls = task_cls
        self.queue_data = queue_data
        self.queue = Queue()
        self.__dict__.update(kwargs)

    @property
    def num_cpus(self):
        return multiprocessing.cpu_count()

    def enqueue(self):
        for obj in self.queue_data:
            self.queue.put(obj)

    def crawl(self, keyword):
        self.task_cls(keyword=keyword,
                      scroll_max=self.__dict__['scroll_max']).crawl()

    def worker(self):
        while not self.queue.empty():
            try:
                keyword = self.queue.get()

                self.crawl(keyword)

                self.queue.task_done()
            except Exception as e:
                l.ERROR(e)
                break

    def start(self):
        self.enqueue()

        for _ in range(self.num_cpus):
            t = Thread(target=self.worker)
            t.deamon = True
            t.start()

        self.queue.join()


