# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from scrape.models import ModelBase, Shop


class Girl(ModelBase):

    id = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=16)
    shop = models.ForeignKey(Shop)
    age = models.PositiveSmallIntegerField()
    img_url = models.CharField(max_length=256)


class Attendance(ModelBase):

    id = models.CharField(primary_key=True, max_length=32)
    girl = models.ForeignKey(Girl, db_index=True)
    date = models.DateField()
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()

    def save(self, **kwargs):
        self.id = Attendance.composite_pk(self.girl.id, self.date)
        super(Attendance, self).save(**kwargs)

    @classmethod
    def composite_pk(cls, girl_id, date):
        return "{0}-{1:%Y%m%d}".format(girl_id, date)


class StatusLog(ModelBase):

    id = models.CharField(primary_key=True, max_length=64)
    attendance = models.ForeignKey(Attendance, db_index=True)
    checked_at = models.DateTimeField()
    status = models.CharField(max_length=8, null=True)

    def save(self, **kwargs):
        self.id = StatusLog.composite_pk(self.attendance.id, self.checked_at)
        super(StatusLog, self).save(**kwargs)

    @classmethod
    def composite_pk(cls, attendance_id, checked_at):
        return "{0}-{1:%H%M%S}".format(
            attendance_id,
            checked_at
        )
