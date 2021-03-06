# coding: utf-8
from __future__ import unicode_literals

from functools32 import lru_cache
from django.db import models
from django_extensions.db.models import TimeStampedModel


class ModelBase(TimeStampedModel):

    class Meta:
        abstract = True

    def __str__(self):
        return "(%s:id=%s)" % (self.__class__.__name__, self.id)

    @classmethod
    def find_by_pk(cls, pk):
        return cls.objects.get(pk=pk)

    @classmethod
    @lru_cache(maxsize=2048)
    def find_by_pk_with_cache(cls, *args, **kw):
        return cls.find_by_pk(*args, **kw)

    @classmethod
    def count(cls):
        return cls.objects.count()


class Shop(ModelBase):

    id = models.CharField(primary_key=True, max_length=64)
    area = models.CharField(max_length=8)

    @classmethod
    def scrapeable(cls):
        return cls.objects.all()
