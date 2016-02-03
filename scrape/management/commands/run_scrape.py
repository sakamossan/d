# coding:utf-8
from __future__ import unicode_literals

import datetime

from django.core.management.base import BaseCommand

from scrape.models import Shop
from scrape.scraper import Page, Scraper
from scrape.helpers import to_biz_date
from jsonl.rw import Writer, jsonl_file_path


class Command(BaseCommand):

    def handle(self, *args, **options):
        biz_date = to_biz_date(datetime.datetime.now())
        file_path = jsonl_file_path(biz_date)
        writer = Writer(file_path)
        for shop in Shop.scrapeable():
            print shop.id  # TODO django-logging
            page = Page(shop)
            scr = Scraper(page)
            data = scr.extract_data()
            writer.write(data)
        writer.file.close()
