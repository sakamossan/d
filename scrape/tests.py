# coding:utf-8
from __future__ import unicode_literals

from .scraper import Page


def test_url():
    p = Page({})
    assert p.url().startswith("http://www")

