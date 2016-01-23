# coding:utf-8
from __future__ import unicode_literals

import datetime
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
