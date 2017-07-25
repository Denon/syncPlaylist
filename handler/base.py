import os
import traceback
import json
import signal
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from settings import *
from utils import _print


class Config(object):
    def __init__(self):
        with open("config.json", 'r') as f:
            account_json = f.read()
        self.config = json.loads(account_json)

    @property
    def account(self):
        return self.config["account"]

    @property
    def password(self):
        return self.config["password"]

    @property
    def source_playlist_url(self):
        return self.config["source_playlist_url"]

    @property
    def target_playlist_url(self):
        return self.config["target_playlist_url"]


class BaseSpider(object):
    def __init__(self):
        self.browser = None
        self.source_playlist = None
        self.target_playlist_tag = None
        self.success_list = list()
        self.failed_list = list()
        self.config = Config()

    def init_browser(self):
        os.environ["webdriver.chrome.driver"] = chrome_driver_path
        os.environ["webdriver.phantomjs.driver"] = phantomjs_driver_path
        # chromedriver = chrome_driver_path
        phantomjs_driver = phantomjs_driver_path

        opts = Options()
        opts.add_argument("user-agent={}".format(headers["User-Agent"]))
        # browser = webdriver.Chrome(chromedriver)
        browser = webdriver.PhantomJS(phantomjs_driver)
        self.browser = browser
        self.wait = ui.WebDriverWait(self.browser, 5)

    def prepare(self):
        pass

    def get_source_playlist(self):
        pass

    def get_target_playlist(self):
        pass

    def sync_song(self):
        pass

    def print_result(self):
        print "total success:{}".format(len(self.success_list))
        print "total failed:{}, detail:".format(len(self.failed_list))
        for failed in self.failed_list:
            _print(failed)

    def run(self):
        try:
            self.prepare()
            self.init_browser()
            self.get_source_playlist()
            self.get_target_playlist()
            self.sync_song()
        except Exception:
            traceback.print_exc()
        finally:
            self.print_result()
            self.browser.service.process.send_signal(signal.SIGTERM)  # kill the specific phantomjs child proc
            self.browser.quit()


