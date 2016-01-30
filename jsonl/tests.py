# coding:utf-8
from __future__ import unicode_literals

import os
import datetime

from jsonl.rw import jsonl_file_path, Writer
from scrape.tests.test_scraper import mocked_scraper


def test_jsonl_file_path():
    assert jsonl_file_path(datetime.date(2016, 3, 27), 'z') == "./resources/jsonl/z20160327.jsonl"


def test_writer():
    path = jsonl_file_path(datetime.datetime(2001, 3, 27), pref='test_')
    try:
        os.remove(path)
    except OSError:
        pass
    wtr = Writer(path)
    scr = mocked_scraper()
    wtr.write(scr.extract_data()[3:7], file_close=True)
    assert 4 == sum(1 for _ in open(path, 'r')), 'written 4 lines'
