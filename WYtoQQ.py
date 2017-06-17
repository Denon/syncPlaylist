# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import traceback
import signal
import functools
import requests
import json
from pprint import pprint
from time import sleep
from urllib import quote
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from settings import *

success_list = list()
failed_list = list()


class Config(object):
    def __init__(self):
        with open("config.json", 'r') as f:
            account_json = f.read()
        self.config = json.loads(account_json)

    @property
    def qq_account(self):
        return self.config["qq_account"]

    @property
    def qq_password(self):
        return self.config["qq_password"]

    @property
    def wy_playlist_url(self):
        playlist_id = self.config["wy_playlist_url"].split("id=")[-1]
        url = "http://music.163.com/playlist?id={}"
        return url.format(playlist_id)

    @property
    def qq_playlist_name(self):
        return self.config["qq_playlist_name"]


config = Config()


def init_browser():
    os.environ["webdriver.chrome.driver"] = chrome_driver_path
    os.environ["webdriver.phantomjs.driver"] = phantomjs_driver_path
    # chromedriver = chrome_driver_path
    phantomjs_driver = phantomjs_driver_path

    opts = Options()
    opts.add_argument("user-agent={}".format(headers["User-Agent"]))
    # browser = webdriver.Chrome(chromedriver)
    browser = webdriver.PhantomJS(phantomjs_driver)
    return browser

browser = init_browser()
wait = ui.WebDriverWait(browser, 5)


class RetryException(Exception):
    pass


def retry(retry_times=0, exc_class=Exception, notice_message=None):
    def wrapper(f):
        @functools.wraps(f)
        def inner_wrapper(*args, **kwargs):
            current = 0
            while True:
                try:
                    return f(*args, **kwargs)
                except exc_class as e:
                    if current >= retry_times:
                        raise RetryException()
                    if notice_message:
                        print notice_message
                    current += 1
        return inner_wrapper
    return wrapper


def get_qq_target_playlist():
    browser.get(qq_playlist_url)
    wait.until(lambda browser: browser.find_element_by_class_name("playlist__list"))
    playlist = browser.find_element_by_class_name("playlist__list")
    playlist_items = playlist.find_elements_by_class_name('playlist__item')

    for item in playlist_items:
        title = item.find_element_by_class_name('playlist__title').text
        item_id = item.get_attribute('data-dirid')
        if title == config.qq_playlist_name:
            return item_id
    else:
        raise Exception("can not find qq playlist:{}, please check".format(config.qq_playlist_name))


def get_163_song_list():

    response = requests.get(config.wy_playlist_url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    details = soup.select("span[class='detail']")
    song_details = list()
    for detail in details:
        song_detail = list()
        song_html_content = detail.contents
        for c in song_html_content:
            if isinstance(c, Tag):
                text = c.text.replace('\n', '')
                song_detail.append(text)

        song = song_detail[0]
        singer, album = song_detail[1].split('- ', 1)
        song_details.append((song, singer, album))
    print "get 163 playlist success"
    return song_details


def search_song(playlist_id, song, singer):
    search_word = "{} {}".format(song, singer)
    url_sw = quote(search_word)
    browser.get(search_url.format(url_sw))
    wait.until(lambda browser: browser.find_element_by_class_name("songlist__list"))
    sleep(1)

    @retry(retry_times=3)
    def _add():
        browser.execute_script("document.getElementsByClassName('songlist__list')[0].firstElementChild.getElementsByClassName('list_menu__add')[0].click()")
        sleep(0.5)
        browser.find_element_by_css_selector("a[data-dirid='{}']".format(playlist_id)).click()
        print "song:{} success".format(song)
        return

    try:
        _add()
    except RetryException:
        print "song:{}, sync error".format(song)
        failed_list.append(search_word)
        return
    else:
        success_list.append(search_word)


@retry(retry_times=3, exc_class=NoSuchElementException, notice_message='login failed and retry')
def login_qq():
    browser.get("https://y.qq.com")
    wait.until(lambda browser: browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/span/a[2]"))
    browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/span/a[2]").click()
    wait.until(lambda browse: browser.find_element_by_id("frame_tips"))
    browser.switch_to.frame("frame_tips")
    wait.until(lambda browse: browser.find_element_by_id("switcher_plogin"))
    sleep(0.5)
    browser.find_element_by_id("switcher_plogin").click()
    user_input = browser.find_element_by_id("u")
    user_input.send_keys(config.qq_account)
    pwd_input = browser.find_element_by_id("p")
    pwd_input.send_keys(config.qq_password)
    submit = browser.find_element_by_id("login_button")
    submit.click()
    sleep(1)
    browser.switch_to.default_content()
    browser.refresh()
    wait.until(lambda browser: browser.find_element_by_class_name("popup_user"))
    user_info = browser.find_element_by_class_name("popup_user")
    user_info.find_element_by_css_selector("*")
    print "login sucess"


def main():
    try:
        song_list = get_163_song_list()
        login_qq()
        target_playlist_id = get_qq_target_playlist()
        for song in song_list:
            search_song(target_playlist_id, song[0], song[1])
    except Exception:
        traceback.print_exc()
    finally:
        print "total success:{}".format(len(success_list))
        print "total failed:{}, detail:".format(len(failed_list))
        pprint(failed_list)
        browser.service.process.send_signal(signal.SIGTERM)  # kill the specific phantomjs child proc
        browser.quit()


if __name__ == '__main__':
    main()


