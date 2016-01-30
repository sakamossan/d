# coding:utf-8
from __future__ import unicode_literals

import datetime

from django.core.management.base import BaseCommand

from scrape.helpers import to_biz_date
from jsonl.rw import Reader, jsonl_file_path
from db.organize import organize_data


class Command(BaseCommand):

    def handle(self, *args, **options):
        biz_date = to_biz_date(datetime.datetime.now())
        file_path = jsonl_file_path(biz_date)
        reader = Reader(file_path)
        [organize_data(line) for line in reader.readlines()]
