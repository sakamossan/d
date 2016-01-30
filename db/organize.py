# coding:utf-8
from __future__ import unicode_literals

from db.models import Girl


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


