# coding:utf-8
from __future__ import unicode_literals
from django.conf import settings
import hypchat


def to_hipchat(*a, **k):
    cli = hypchat.HypChat(settings.V2_HIPCHAT_TOKEN)
    room = cli.get_room(settings.D_ROOM_ID)
    # https://www.hipchat.com/docs/apiv2/method/send_room_notificatio
    # eg,| room.notification(html from='bot', color='gray', message_format='html')
    room.notification(*a, **k)
