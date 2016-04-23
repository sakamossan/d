# coding:utf-8
from __future__ import unicode_literals

import mock
import functools32
from scrape.models import Shop
from scrape.scraper import Page, Scraper


@functools32.lru_cache()
def mocked_scraper(shop_id='hp'):
    with open('resources/tests/{}.html'.format(shop_id)) as f:
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


def test_not_girl_exception():

    scr = mocked_scraper('gingira')
    not_girl = scr.distribute_extractors()[0]
    assert not_girl.extract() == 'http://www.cityheaven.net/tt/gingira/A6GirlDetailProfile/?girlId=10382291'

