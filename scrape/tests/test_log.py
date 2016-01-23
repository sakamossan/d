# coding:utf-8
from __future__ import unicode_literals

import os
import datetime
from scrape.log import jlfile_path, Writer
from scrape.tests.test_scraper import mocked_scraper


def test_logfile_path():
    assert jlfile_path(datetime.date(2016, 3, 27), 'z') == "./log/z20160327.jl"


def test_writer():
    path = jlfile_path(datetime.datetime(2001, 3, 27), pref='test_')
    os.remove(path)
    wtr = Writer(path)
    scr = mocked_scraper()
    wtr.write_jsonlines(scr.extract_data()[3:7])
    assert 4 == sum(1 for _ in open(path, 'r')), '全部で4行'
