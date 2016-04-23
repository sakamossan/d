# coding:utf-8
from __future__ import unicode_literals

import re
import urllib2
import bs4
import datetime

from scrape.helpers import clock_to_datetime, current_term


# 最低限検索に引っかからないようにする
caesar = lambda s: "".join([chr(ord(c)+3) for c in s])


class Page(object):

    urlfmt = caesar('eqqm7,,ttt+`fqveb^sbk+kbq,xz,xz,>4PerhhfkVlqbf,<ploqjlab:-')

    def __init__(self, shop):
        self.shop = shop

    def url(self):
        s = self.shop
        return self.urlfmt.format(s.area, s.id)

    def get_html(self):
        res = urllib2.urlopen(self.url())
        return res.read()


class Scraper(object):

    def __init__(self, page):
        """:type page: Page"""
        self.root = bs4.BeautifulSoup(page.get_html(), "html.parser")

    def distribute_extractors(self):
        """:rtype: list[Extractor]"""
        return [
            Extractor(chunk) for chunk
            in self.root.findAll("div", attrs={"id": "shukkin_list"})
        ]

    def extract_data(self):
        return filter(bool, [e.extract() for e in self.distribute_extractors()])


class ExtractException(ValueError):
    pass


class Extractor(object):

    def __init__(self, bs_chunk):
        """:type bs_chunk: BeautifulSoup"""
        self.chunk = bs_chunk
        self.chunk_branch = self.chunk.findAll("tr")[-1]

    def extract(self):
        in_, out = self.get_clock_in_out()
        try:
            return {
                'girl_id': self.get_girl_id(),
                'name': self.get_name(),
                'age': self.get_age(),
                'img_url': self.get_img_url(),
                'shop_id': self.get_shop_id(),

                'status': self.get_status(),
                'clock_in': in_,
                'clock_out': out,
                'checked_term': current_term()
            }
        except ExtractException:
            base = "http://www.cityheaven.net/tt/{}/A6GirlDetailProfile/?girlId={}"
            ret = base.format(self.get_shop_id(), self.get_girl_id())
            print ret  # TODO logging
            return ret

    def get_age(self):
        txt = self.chunk.find("th").text
        if '割】' in txt:
            # gingira?
            raise ExtractException
        found = re.findall(r'\d{2}', txt)
        if not found:
            # honeyplaza?
            raise ExtractException
        return int(found[0])

    def get_status(self, now=None):
        # TODO statusの仕様とテストを決める

        in_, out = self.get_clock_in_out()
        if in_ is None and out is None:
            # 勤務時間がわからない人はstatusをNoneにする
            return None

        now = now or datetime.datetime.now()
        if not (in_ < now < out):
            # 勤務時間外
            return "off"

        txt = self.chunk.text
        if "受付終了" in txt:
            # 予約でいっぱいという状態なので終業時間までは仕事中と判定する
            return "work"
        elif "現在待機中" in txt:
            # 待ちの状態
            return "wait"
        else:
            # それ以外の状態 おそらく仕事中?
            return "work"

    def get_img_url(self):
        return self.chunk.find("img")['src'].replace("sn_", "")

    def get_shop_id(self):
        return self.get_img_url().split("/")[6]

    def get_name(self):
        return self.chunk_branch.find("img")['alt']

    def get_girl_id(self):
        return self.chunk_branch.find("a")['href'].split("=")[-1]

    def get_clock_in_out(self):
        clocks_text = self.chunk_branch.findAll("td", attrs={"width": "110"})[0].text
        clocks = re.findall("(\d{1,2}:\d{1,2})", clocks_text)
        # 全て休日になっている場合は勤務時間が取得できない
        return map(clock_to_datetime, clocks) or [None, None]
