# coding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from d.notify import HipChatNotifier


class Command(BaseCommand):

    def handle(self, *args, **options):
        hc = HipChatNotifier()
        hc.notification()
