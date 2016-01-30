# coding: utf-8
from __future__ import unicode_literals

import datetime
from django.test import TestCase
from scrape.models import Shop
from db.models import Girl, Attendance, StatusLog


class TestSaves(TestCase):

    fixtures = ['scrape.json']

    def test_saves(self):
        girl = Girl.objects.create(
            id='1000000000',
            shop=Shop.find_by_pk('honeyplaza'),
            name='てす子',
            age=23,
            img_url='http://example.com/tesko.jpg'
        )
        atnd = Attendance.objects.create(
            girl=girl,
            date=datetime.date(2016, 2, 2),
            clock_in=datetime.datetime(2016, 2, 2, 20, 30, 0),
            clock_out=datetime.datetime(2016, 2, 3, 3, 0, 0)
        )
        log = StatusLog.objects.create(
            attendance=atnd,
            checked_at=datetime.datetime(2016, 2, 2, 20, 30, 0),
            status='work',
        )
        self.assertEqual(log.id, '1000000000-20160202-203000')
