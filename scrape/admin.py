# coding:utf-8
from __future__ import unicode_literals

from django.contrib import admin
from scrape.models import Shop, BlackList

admin.site.register(Shop)
admin.site.register(BlackList)
