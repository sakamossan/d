# coding:utf-8
from __future__ import unicode_literals

from scrape.helpers import to_biz_date
from db.models import Girl, Attendance


def organize_data(data):
    pass


class Organizer(object):

    def organize(self, data):
        pass

    def process_girl(self, data):
        """:rtype: (Girl, bool)"""
        try:
            girl_id = data['girl_id']
            return Girl.find_by_pk_with_cache(girl_id), False
        except Girl.DoesNotExist:
            girl = Girl()
            girl.id = data['girl_id']
            girl.name = data['name']
            girl.age = data['age']
            girl.shop_id = data['shop_id']
            girl.img_url = data['img_url']
            girl.save()
            return girl, True

    def process_attendance(self, data):
        """:rtype: (Attendance, bool)"""
        try:
            pk = Attendance.composite_pk(
                data['girl_id'],
                to_biz_date(data['checked_term']))
            return Attendance.find_by_pk_with_cache(pk), False
        except Attendance.DoesNotExist:
            atnd = Attendance()
            atnd.girl = Girl.find_by_pk_with_cache(data['girl_id'])
            atnd.date = to_biz_date(data['checked_term'])
            atnd.clock_in = data['clock_in']
            atnd.clock_out = data['clock_out']
            atnd.save()
            return atnd, True
