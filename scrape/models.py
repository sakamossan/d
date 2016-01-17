# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel


class ModelBase(TimeStampedModel):
    """プロジェクト内で共通して使用するベースクラス"""

    class Meta:
        abstract = True

    def __str__(self):
        return "(%s:id=%s)" % (self.__class__.__name__, self.id)

