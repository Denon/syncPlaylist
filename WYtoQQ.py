import urlparse
from time import sleep
from base import BaseSpider
import requests
from bs4 import BeautifulSoup
from settings import *
from urllib2 import quote

from api.wy import get_playlist_detail
from utils import _print, retry, RetryException


class WYtoQQ(BaseSpider):
    @retry(retry_times=3, notice_message="login failed and retry")
    def prepare(self):
        self.browser.get("https://y.qq.com")
        self.browser.set_window_size(1920, 1080)
        self.wait.until(lambda browser: browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/span/a[2]"))
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/span/a[2]").click()
        self.wait.until(lambda browser: browser.find_element_by_id("frame_tips"))
        self.browser.switch_to.frame("frame_tips")
        self.wait.until(lambda browser: browser.find_element_by_id("switcher_plogin"))
        sleep(0.5)
        self.browser.find_element_by_id("switcher_plogin").click()
        user_input = self.browser.find_element_by_id("u")
        user_input.send_keys(self.config.account)
        pwd_input = self.browser.find_element_by_id("p")
        pwd_input.send_keys(self.config.password)
        submit = self.browser.find_element_by_id("login_button")
        submit.click()
        sleep(1)
        self.browser.switch_to.default_content()
        self.browser.refresh()
        self.wait.until(lambda browser: browser.find_element_by_class_name("popup_user"))
        user_info = self.browser.find_element_by_class_name("popup_user")
        user_info.find_element_by_css_selector("*")
        print("login sucess")

    def get_source_playlist(self):
        url = self.config.source_playlist_url.replace('#', 'm')
        parse_url = urlparse.urlparse(url)
        playlist_id = urlparse.parse_qs(parse_url.query)["id"][0]
        detail = get_playlist_detail(playlist_id)
        song_list = detail['playlist']['tracks']
        song_details = list()
        for song in song_list:
            ar_name = list()
            song_name = song['name']
            for ar in song['ar']:
                ar_name.append(ar['name'])
            album = ''
            song_details.append((song_name, ' '.join(ar_name), album))
        # response = requests.get(self.config.source_playlist_url.replace('#', 'm'), headers=headers)
        # html = response.content
        # soup = BeautifulSoup(html, "html.parser")
        # details = soup.select("span[class='detail']")
        # song_details = list()
        # for detail in details:
        #     song_text = detail.text
        #     song_detail = song_text.strip('\n').split('\n\n')
        #
        #     song = song_detail[0]
        #     singer = song_detail[1].split('- ', 1)[0]
        #     # don't use album yet
        #     album = ''
        #     song_details.append((song, singer.strip('\n'), album))
        print("get 163 playlist success")
        self.source_playlist = song_details

    def get_target_playlist(self):
        # self.browser.get(self.config.target_playlist_url)
        # self.wait.until(lambda browser: browser.find_element_by_class_name("playlist__list"))
        # playlist = self.browser.find_element_by_class_name("playlist__list")
        # playlist_items = playlist.find_elements_by_class_name('playlist__item')
        #
        # for item in playlist_items:
        #     title = item.find_element_by_class_name('playlist__title').text
        #     item_id = item.get_attribute('data-dirid')
        #     if title == self.config.qq_playlist_name:
        #         self.target_playlist_tag = item_id
        #         return
        # else:
        #     raise Exception("can not find qq playlist:{}, please check".format(self.config.qq_playlist_name))
        self.target_playlist_tag = self.config.target_playlist_url.split('dirid=')[-1]
        return

    def sync_song(self):
        for song_detail in self.source_playlist:
            song = song_detail[0]
            singer = song_detail[1]
            search_word = u"{} {}".format(song, singer)
            url_sw = quote(search_word.encode('utf8'))
            self.browser.get(qq_search_url.format(url_sw))
            self.wait.until(lambda browser: browser.find_element_by_class_name("songlist__list"))
            sleep(0.5)

            @retry(retry_times=3)
            def _add(browser):
                browser.execute_script("document.getElementsByClassName('songlist__list')[0].firstElementChild.getElementsByClassName('list_menu__add')[0].click()")
                sleep(0.5)
                browser.find_element_by_css_selector("a[data-dirid='{}']".format(self.target_playlist_tag)).click()
                _print(u"song:{} success".format(song))

            try:
                _add(self.browser)
            except RetryException:
                _print(u"song:{}, sync error".format(song))
                self.failed_list.append(search_word)
            else:
                self.success_list.append(search_word)

if __name__ == '__main__':
    WYtoQQ().run()
