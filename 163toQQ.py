# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import traceback
import signal
import functools
import requests
from time import sleep
from urllib import quote
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from config import *


headers = {
    "User-Agent": 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.'
}

url = "http://music.163.com/playlist?id=31421765"
search_url = "https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w={}"
target_playlist_name = 'test1'


os.environ["webdriver.chrome.driver"] = "/Users/denon/Downloads/chromedriver"
os.environ["webdriver.phantomjs.driver"] = phantomjs_driver_path
chromedriver = "/Users/denon/Downloads/chromedriver"
phantomjs_driver = phantomjs_driver_path

opts = Options()
opts.add_argument("user-agent={}".format(headers["User-Agent"]))
browser = webdriver.Chrome(chromedriver)
# browser = webdriver.PhantomJS(phantomjs_driver)
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
                    print notice_message
                    current += 1
        return inner_wrapper
    return wrapper


def get_qq_target_playlist():
    browser.get('https://y.qq.com/portal/profile.html#sub=other&tab=create&')
    wait.until(lambda browser: browser.find_element_by_class_name("playlist__list"))
    playlist = browser.find_element_by_class_name("playlist__list")
    playlist_items = playlist.find_elements_by_class_name('playlist__item')

    for item in playlist_items:
        title = item.find_element_by_class_name('playlist__title').text
        item_id = item.get_attribute('data-dirid')
        if title == target_playlist_name:
            return item_id


def get_163_song_list():
    response = requests.get(url, headers=headers)
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
    return song_details


def search_song(playlist_id, song, singer):
    print song
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
        return


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
    user_input.send_keys(qq_account.account)
    pwd_input = browser.find_element_by_id("p")
    pwd_input.send_keys(qq_account.password)
    submit = browser.find_element_by_id("login_button")
    submit.click()
    sleep(1)
    browser.switch_to.default_content()
    browser.refresh()
    wait.until(lambda browser: browser.find_element_by_class_name("popup_user"))
    user_info = browser.find_element_by_class_name("popup_user")
    user_info.find_element_by_css_selector("*")
    print "login sucess"


if __name__ == '__main__':
    try:
        song_list = get_163_song_list()
        login_qq()
        target_playlist_id = get_qq_target_playlist()
        for song in song_list:
            search_song(target_playlist_id, song[0], song[1])
    except Exception as e:
        traceback.print_exc()
    finally:
        browser.service.process.send_signal(signal.SIGTERM)  # kill the specific phantomjs child proc
        browser.quit()


