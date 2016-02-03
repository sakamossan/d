# coding:utf-8
from __future__ import unicode_literals

import os
import datetime

from jsonl.rw import jsonl_file_path, Writer, Reader
from scrape.tests.test_scraper import mocked_scraper


def dummy_data():
    path = './resources/tests/test_20010327.jsonl'
    rdr = Reader(path)
    return list(rdr.readlines())


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


def test_reader():
    path = './resources/tests/test_20010327.jsonl'
    rdr = Reader(path)
    assert 4 == sum(1 for _ in rdr.readlines()), 'read 4 lines'
