# coding:utf-8
from __future__ import unicode_literals

import glob
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):

    def handle(self, *args, **options):

        for path in glob.glob('./resources/view_sqls/*'):
            ddl = open(path).read()
            cur = connection.cursor()
            cur.execute(ddl)
