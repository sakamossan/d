# coding:utf-8
from __future__ import unicode_literals

from django.db.utils import IntegrityError
from scrape.helpers import to_biz_date
from db.models import Girl, Attendance, StatusLog


class InvalidDataException(BaseException):
    pass


class NotOurDataException(BaseException):
    pass


class Organizer(object):

    def organize(self, data):
        try:
            self.process_girl(data)
            self.process_attendance(data)
            self.process_status_log(data)
        except NotOurDataException:
            pass

    def save_or_raise(self, obj):
        try:
            obj.save()
        except (IntegrityError, ValueError):
            raise InvalidDataException

    def process_girl(self, data):
        """:rtype: (Girl, bool)"""
        try:
            girl_id = data['girl_id']
            return Girl.find_by_pk_with_cache(girl_id), False
        except Girl.DoesNotExist:
            girl = Girl()
            girl.id = data['girl_id']
            girl.name = data['name']
            girl.age = data.get('age')
            girl.shop_id = data.get('shop_id')
            girl.img_url = data['img_url']
            self.save_or_raise(girl)
            return girl, True

    def process_attendance(self, data):
        """:rtype: (Attendance, bool)"""
        if data.get('clock_in') is None or data.get('clock_out') is None:
            raise NotOurDataException

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
            self.save_or_raise(atnd)
            return atnd, True

    def process_status_log(self, data):
        """:rtype: (StatusLog, bool)"""
        if not data.get('status') in ('off', 'work', 'wait'):
            raise NotOurDataException

        checked_at = data.get('checked_term')
        atnd_id = Attendance.composite_pk(
            data['girl_id'],
            to_biz_date(checked_at))
        try:
            pk = StatusLog.composite_pk(atnd_id, checked_at)
            return StatusLog.find_by_pk_with_cache(pk), False
        except StatusLog.DoesNotExist:
            stat = StatusLog()
            stat.attendance = Attendance.find_by_pk_with_cache(atnd_id)
            stat.checked_at = checked_at
            stat.status = data['status']
            self.save_or_raise(stat)
            return stat, True
