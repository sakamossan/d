# coding:utf-8
from __future__ import unicode_literals

# coding:utf-8

import re
import datetime


# 現システムでは03:00 ~ 09:00という勤務時間は例外とする
TomorrowHour = 6


def norm_datetime(dt, interval=5):
    """
    分単位まで見て、一番近いn分刻みのdatetimeに正規化する
    たとえば17時23分を5分単位で正規化すると17時25分となる

    :param interval: int
    :return: datetime.datetime
    """
    cur = 0
    while interval / 2.0 < abs(dt.minute - cur):
        cur += interval
    else:
        return dt.replace(minute=cur, second=0, microsecond=0)


def current_term():
    return norm_datetime(datetime.datetime.now(), 5)


def to_biz_date(dtm):
    """
    >>> to_biz_date(datetime.datetime(2015, 12, 2, 2, 0, 0))
    datetime.date(2015, 12, 1)

    システム上、6時から翌日と考える

    ufo曰く:
        そこは業態によっても多少違うのですが、
        通常6時(日の出時刻)が出勤の開始で、5時が終了だと考えていいと思います。

        ソープ：日の出開始ー12時終了
        デリヘル：(通常)10時開始-5時終わり(これより時間が短い店も多いです。)

    :param dtm: datetime.datetime
    :return: datetime.date
    """
    is_am_midnight = int(dtm.hour < TomorrowHour)
    return (dtm - datetime.timedelta(days=is_am_midnight)).date()


def clock_to_datetime(clock, now=None):
    """
    `18:30`といった表記をdatetimeに変換する
    to_biz_dateと同様に6時から翌日と考える

    :param clock: string ex.) 05:30
    :param now: datetime.datetime
    :return: datetime.datetime
    """
    tm = datetime.time(*map(int, clock.split(":")))
    biz_dt = to_biz_date(now or datetime.datetime.now())
    if tm < datetime.time(hour=TomorrowHour):
        # 00:00 ~ 05:59
        biz_dt += datetime.timedelta(days=1)
    return datetime.datetime.combine(biz_dt, tm)


def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, basestring) and re.search("^\d{4}-\d{2}-\d{2}", v):
            try:
                dct[k] = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
            except:
                pass
    return dct


if __name__ == "__main__":
    import doctest
    doctest.testmod()

