# coding:utf-8
from __future__ import unicode_literals

import datetime
import mock
import functools32
from scrape.models import Shop
from scrape.scraper import Page, Scraper


@functools32.lru_cache()
def mocked_scraper():
    with open('resources/tests/hp.html') as f:
        html = f.read()
    page = mock.Mock()
    page.get_html.return_value = html
    return Scraper(page)


def test_url():
    shop = Shop(id='test-id', area='tt')
    p = Page(shop)
    assert p.url().startswith("http://www")
    assert "test-id" in p.url()


def test_scraper():
    scr = mocked_scraper()
    exs = scr.distribute_extractors()
    assert len(exs) == 30


def test_extractor():
    scr = mocked_scraper()
    extrs = scr.distribute_extractors()
    assert extrs[0].get_age() == 23

    assert all([
        'pc.jpg' in e.get_img_url()
        for e in extrs]), '全員jpg形式で画像がある'

    assert all([
        'honey' in e.get_shop_id()
        for e in extrs]), '全員お店のIDがちゃんととれているか'

    assert extrs[-1].get_name() == 'さゆ'

    assert extrs[-2].get_girl_id() == '11466734'

    ids = [e.get_girl_id() for e in extrs]
    assert len(ids) == len(set(ids)), '嬢全員に異なるIDがふられている'

    # TODO test get_status


from scrape.helpers import (
    to_biz_date, norm_datetime, clock_to_datetime
)


def test_to_business_day():
    assert datetime.date(2015, 12, 1) == \
        to_biz_date(datetime.datetime(2015, 12, 1, 23, 59, 59))

    assert datetime.date(2015, 12, 1) == \
        to_biz_date(datetime.datetime(2015, 12, 2, 0, 0, 0))

    assert datetime.date(2015, 12, 1) == \
        to_biz_date(datetime.datetime(2015, 12, 2, 5, 59, 59))

    assert datetime.date(2015, 12, 2) == \
        to_biz_date(datetime.datetime(2015, 12, 2, 6, 0, 0))


def test_norm_datetime():
    assert datetime.datetime(2015, 12, 1, 12, 15) == \
        norm_datetime(datetime.datetime(2015, 12, 1, 12, 17, 29))

    assert datetime.datetime(2015, 12, 1, 12, 15) == \
        norm_datetime(datetime.datetime(2015, 12, 1, 12, 17, 30))

    assert datetime.datetime(2015, 12, 1, 12, 20) == \
        norm_datetime(datetime.datetime(2015, 12, 1, 12, 18, 0))


def test_clock_to_datetime():
    n23 = datetime.datetime(2015, 12, 1, 23, 00)
    assert clock_to_datetime("18:30", n23) == datetime.datetime(2015, 12, 1, 18, 30)
    assert clock_to_datetime("05:30", n23) == datetime.datetime(2015, 12, 2, 5, 30)
    assert clock_to_datetime("06:00", n23) == datetime.datetime(2015, 12, 1, 6, 00), \
        '夜23時に`06:00`という時刻を観測したら、それはその日の朝だとみなす'

    n6 = datetime.datetime(2015, 12, 2, 6, 00)
    assert clock_to_datetime("06:00", n6) == datetime.datetime(2015, 12, 2, 6, 00)
    assert clock_to_datetime("18:30", n6) == datetime.datetime(2015, 12, 2, 18, 30)
    assert clock_to_datetime("05:30", n6) == datetime.datetime(2015, 12, 3, 5, 30), \
        '朝の6時に`05:30`という時刻を観測したら、それは翌日の深夜だとみなす'
