# coding: utf-8
from __future__ import unicode_literals

import datetime
from django.test import TestCase
from scrape.models import Shop
from jsonl.tests import dummy_data
from db.models import Girl, Attendance, StatusLog
from db.organize import Organizer


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


class TestOrganizer(TestCase):

    fixtures = ['scrape.json']

    def setUp(self):
        self.org = Organizer()
        self.data = dummy_data()

    def test_process_girl(self):
        datum = self.data[0]

        # first
        girl, is_new = self.org.process_girl(datum)
        self.assertTrue(is_new)
        self.assertEqual(girl.id, '12285394')
        self.assertEqual(girl.name, 'エルメ')
        self.assertEqual(girl.age, 23)
        self.assertEqual(girl.shop_id, 'honeyplaza')
        self.assertTrue('grpb0012285394_0000000000pc.jpg?cache02=1453258218' in girl.img_url)

        # second
        girl, is_not_new = self.org.process_girl(datum)
        self.assertFalse(is_not_new)
        self.assertEqual(girl.id, '12285394')

        # count-inserted
        self.assertEqual(Girl.count(), 1)

    def test_process_attendance(self):
        datum = self.data[1]

        # exercise
        self.org.process_girl(datum)

        # first
        atnd, is_new = self.org.process_attendance(datum)
        self.assertTrue(is_new)
        self.assertEqual(atnd.id, '12192627-20160130')
        self.assertEqual(atnd.girl.id, '12192627')
        self.assertEqual(atnd.date, datetime.date(2016, 1, 30))
        self.assertEqual(atnd.clock_in, datetime.datetime(2016, 1, 30, 18, 0, 0))
        self.assertEqual(atnd.clock_out, datetime.datetime(2016, 1, 31, 2, 0, 0))

        # second
        snd, is_not_new = self.org.process_attendance(datum)
        self.assertFalse(is_not_new)
        self.assertEqual(snd.id, '12192627-20160130')

        # count-inserted
        self.assertEqual(Attendance.count(), 1)



